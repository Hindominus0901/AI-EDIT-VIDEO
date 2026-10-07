import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import user_profile as profiles

def script(name):
    spec=importlib.util.spec_from_file_location(name.replace('-','_'),ROOT/'scripts'/f'{name}.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module

class ProfileTests(unittest.TestCase):
    def test_fresh_user_gets_vietnamese_defaults_without_write(self):
        with tempfile.TemporaryDirectory() as tmp:
            effective=profiles.resolve(profiles.read_profile(tmp,'kenh-moi'),{})
            self.assertEqual(effective['interfaceLanguage'],'vi')
            self.assertEqual(effective['style'],'studio')
            self.assertFalse((Path(tmp)/'.video-editor').exists())

    def test_persistence_across_processes_and_channels(self):
        with tempfile.TemporaryDirectory() as tmp:
            patch_file=Path(tmp)/'preferences.json';patch_file.write_text(json.dumps({'style':'clean','music':'none'}),encoding='utf-8')
            common=[sys.executable,str(ROOT/'scripts/user_profile.py')]
            subprocess.run([*common,'save','--workspace',tmp,'--channel','kien-thuc','--input',str(patch_file)],capture_output=True,check=True)
            result=subprocess.run([*common,'resolve','--workspace',tmp,'--channel','kien-thuc'],capture_output=True,check=True,encoding='utf-8')
            self.assertEqual(json.loads(result.stdout)['style'],'clean')
            self.assertEqual(profiles.read_profile(tmp,'khach-khac')['preferences'],{})
            saved=profiles.read_profile(tmp,'kien-thuc')['preferences']
            self.assertEqual(saved,{'style':'clean','music':'none'})

    def test_one_off_override_does_not_change_saved_profile(self):
        with tempfile.TemporaryDirectory() as tmp:
            profile=profiles.save_profile(tmp,'kien-thuc',{'style':'clean','aspect':'9:16'})
            before=copy.deepcopy(profile)
            result=profiles.resolve(profile,{'aspect':'16:9','avoid':['chữ che mặt']})
            result['avoid'].append('nhạc lớn')
            self.assertEqual(profile,before)
            self.assertEqual(result['aspect'],'16:9')
            self.assertEqual(profiles.read_profile(tmp,'kien-thuc'),before)

    def test_invalid_channel_and_preferences_cannot_write(self):
        with tempfile.TemporaryDirectory() as tmp:
            for channel in ['../escape','C:/escape','con','a/b','', 'A']:
                with self.assertRaises(ValueError):profiles.save_profile(tmp,channel,{'style':'studio'})
            for prefs in [{'style':'neon'},{'targetDurationSec':True},{'targetDurationSec':float('nan')},{'unknown':1},{'avoid':'abc'}]:
                with self.assertRaises(ValueError):profiles.save_profile(tmp,'kenh',prefs)
            self.assertFalse((Path(tmp)/'.video-editor').exists())

class RuntimeTests(unittest.TestCase):
    def test_render_mode_does_not_require_transcription(self):
        doctor=script('doctor')
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            for file in ['node_modules/remotion/package.json','src/Root.tsx','scripts/render-edit.py']:
                p=root/file;p.parent.mkdir(parents=True,exist_ok=True);p.write_text('')
            with patch.object(doctor,'version_of',side_effect=lambda cmd:'v24.1.0' if cmd[0]=='node' else 'ffmpeg test'),patch.object(doctor.importlib.util,'find_spec',return_value=None):
                self.assertTrue(doctor.collect('render',root)['ready'])
                self.assertFalse(doctor.collect('all',root)['ready'])
                self.assertFalse(doctor.collect('render',root)['transcribeDependenciesReady'])

    def test_missing_ffmpeg_blocks_even_render_mode(self):
        doctor=script('doctor')
        with patch.object(doctor,'version_of',return_value=None):
            self.assertFalse(doctor.collect('render')['ready'])

    def test_failed_version_command_is_not_ready(self):
        doctor=script('doctor')
        with patch.object(doctor.shutil,'which',return_value='node'),patch.object(doctor.subprocess,'run') as run:
            run.return_value.returncode=1;run.return_value.stdout='v24.0.0';run.return_value.stderr=''
            self.assertIsNone(doctor.version_of(['node','--version']))

class ProjectIsolationTests(unittest.TestCase):
    def test_pipeline_routes_all_stages_and_reuses_stt_cache(self):
        pipeline=script('run-pipeline')
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);public=root/'public';scripts=root/'scripts'
            scripts.mkdir();(scripts/'transcribe.py').write_text('cache fingerprint')
            calls=[]
            transcript={'durationSec':3,'words':[]}
            def fake_run(cmd,**kwargs):
                calls.append(cmd)
                if str(cmd[0])=='ffmpeg':Path(cmd[-1]).write_bytes(b'audio')
                elif str(cmd[1]).endswith('transcribe.py'):
                    Path(cmd[cmd.index('--out')+1]).write_text(json.dumps(transcript),encoding='utf-8')
                elif str(cmd[1]).endswith('silence-cut.py'):
                    out=Path(cmd[cmd.index('--out-dir')+1])
                    (out/'transcript-tight.json').write_text(json.dumps(transcript),encoding='utf-8')
                    (out/'tight.mp4').write_bytes(b'tight')
                    (out/'cut-report.json').write_text(json.dumps({'removedSec':0,'removedPct':0,'segments':1}))
            for project in ['first','second']:
                clip=public/f'raw/{project}/source.mp4';clip.parent.mkdir(parents=True);clip.write_bytes(b'same original media')
                args=['run-pipeline',f'raw/{project}/source.mp4','--out-dir',f'out/{project}','--llm','offline']
                with patch.object(pipeline,'ROOT',root),patch.object(pipeline,'PUBLIC',public),patch.object(pipeline,'SCRIPTS',scripts),patch.object(pipeline,'run',side_effect=fake_run),patch.object(sys,'argv',args):pipeline.main()
                self.assertEqual((public/f'raw/{project}/source-tight.mp4').read_bytes(),b'tight')
                self.assertTrue((root/f'out/{project}/transcript-source.json').is_file())
            stt=[c for c in calls if len(c)>1 and str(c[1]).endswith('transcribe.py')]
            self.assertEqual(len(stt),1)
            self.assertFalse((root/'out/transcript.json').exists())
            self.assertFalse((public/'raw/source-tight.mp4').exists())
            for c in calls:
                if len(c)>1 and any(str(c[1]).endswith(name) for name in ['silence-cut.py','detect-face-zones.py','generate-edl.py']):
                    self.assertIn('--out-dir',c)

    def test_pure_edit_no_cache_transcribes_fresh_and_writes_no_cache(self):
        pipeline=script('run-pipeline')
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);public=root/'public';scripts=root/'scripts'
            scripts.mkdir();(scripts/'transcribe.py').write_text('cache fingerprint')
            calls=[];transcript={'durationSec':3,'words':[]}
            def fake_run(cmd,**kwargs):
                calls.append(cmd)
                if str(cmd[0])=='ffmpeg':Path(cmd[-1]).write_bytes(b'audio')
                elif str(cmd[1]).endswith('transcribe.py'):
                    Path(cmd[cmd.index('--out')+1]).write_text(json.dumps(transcript),encoding='utf-8')
            clip=public/'raw/pure/source.mp4';clip.parent.mkdir(parents=True);clip.write_bytes(b'fresh media')
            for project in ['pure-a','pure-b']:
                args=['run-pipeline','raw/pure/source.mp4','--out-dir',f'out/{project}',
                      '--llm','offline','--keep-silence','--no-cache']
                with patch.object(pipeline,'ROOT',root),patch.object(pipeline,'PUBLIC',public),patch.object(pipeline,'SCRIPTS',scripts),patch.object(pipeline,'run',side_effect=fake_run),patch.object(sys,'argv',args):
                    pipeline.main()
            stt=[c for c in calls if len(c)>1 and str(c[1]).endswith('transcribe.py')]
            self.assertEqual(len(stt),2)
            self.assertFalse((root/'.cache').exists())

    def test_private_material_is_excluded_from_release(self):
        pack=script('pack-kit');files=pack.selected_files()
        forbidden={'out','raw','goldens','.video-editor','.cache','.env','.venv','node_modules'}
        self.assertTrue(files)
        self.assertFalse(any(forbidden.intersection(p.parts) for p in files))
        self.assertFalse(any('.claude/agents' in p.as_posix() for p in files))
        self.assertFalse(any('STYLE-PREFERENCES' in p.as_posix() for p in files))
        self.assertIn(Path('scripts/user_profile.py'),files)
        self.assertIn(Path('asset-library/licenses/Kenney-License.txt'),files)

if __name__=='__main__':unittest.main()
