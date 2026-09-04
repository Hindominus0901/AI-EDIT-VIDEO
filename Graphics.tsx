/**
 * Motion-graphic overlays mapped from EDL graphics track.
 * hook (spring scale-in title), cta (end call-to-action), kinetic (per-word bounce),
 * lower-third (handle). Each driven by useCurrentFrame + spring/interpolate.
 */
import React from "react";
import {
  AbsoluteFill,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import type { Graphic } from "../edl-types";
import {
  AnimatedCallout,
  HighlightReveal,
  NumberCounter,
  ProgressBar,
  BadgePop,
} from "./MotionGraphics";
import { GlassCard } from "./AdvancedLayouts";
import { DonutStat, BarStat } from "./Charts";
import { KineticStatement, MaskReveal, GlassStrip } from "./KineticTypo";
import { PathMark } from "./PathMarks";
import { Shape3D } from "./Shape3D";
import { IllusMark } from "./Elements";
import { StepFlow, Comparison, ListReveal, LowerThirdPro } from "./Infographic";
import { InfoTable, StatCompare } from "./DataViz";
import {
  DiamondLabel,
  DualIconCards,
  NegativeSlashCard,
  NeonIconCard,
  PremiumRoadmap,
} from "./PremiumVisuals";
import { AdComparisonScene } from "./TobiAdVisuals";
import { enterExit, popSpring, floatY, glow } from "../anim";
import { topBandStyle, bottomBandStyle, centerStyle } from "../layout";
import { DISPLAY_FONT, VI_SAFE_LINE_HEIGHT, VI_DIACRITIC_PAD } from "../fonts";
import { useStyle } from "../style-context";
import { pickEmphasisIndex } from "../text-emphasis";
import { BrollHookTitle, BrollSubHook, BrollCta } from "./BrollHook";

export const GraphicLayer: React.FC<{ graphic: Graphic; accent: string; accent2: string }> = ({
  graphic,
  accent,
  accent2,
}) => {
  const recipe = useStyle();
  const scale = Math.min(1, Math.max(0.45, recipe.textScale));
  let node: React.ReactNode = null;
  switch (graphic.type) {
    case "hook":
      node = <HookTitle text={graphic.text} accent={accent} accent2={accent2} />;
      break;
    case "cta":
      node = <CtaEnd text={graphic.text} accent={accent} accent2={accent2} />;
      break;
    case "kinetic":
      node = <KineticText text={graphic.text} accent={accent} />;
      break;
    case "lower-third":
      node = <LowerThird text={graphic.text} accent={accent} />;
      break;
    case "callout":
      // warningMode (GROUP 1): alert-red accent instead of the theme accent
      node = <AnimatedCallout text={graphic.text} accent={graphic.warningMode ? "#EF4444" : accent} anchor={graphic.anchor} />;
      break;
    case "highlight-reveal":
      node = <HighlightReveal text={graphic.text} accent={accent} />;
      break;
    case "number-counter":
      node = (
        <NumberCounter
          value={graphic.value ?? 0}
          suffix={graphic.suffix}
          label={graphic.label}
          accent={accent}
        />
      );
      break;
    case "progress-bar":
      node = <ProgressBar accent={accent} label={graphic.label} />;
      break;
    case "badge":
      node = <BadgePop text={graphic.text} accent={accent} />;
      break;
    case "color-wipe":
      // ColorWipe removed from the system: a full-frame color plate over the
      // speaker reads as a render glitch; legacy entries render nothing
      node = null;
      break;
    // ---- b-roll hook stack (workflow B) ----
    case "broll-hook":
      node = (
        <BrollHookTitle
          lines={graphic.items?.length ? graphic.items : graphic.text.split("|").map((s) => s.trim()).filter(Boolean)}
          accent={accent}
        />
      );
      break;
    case "broll-subhook":
      node = <BrollSubHook text={graphic.text} />;
      break;
    case "broll-cta":
      node = <BrollCta text={graphic.text} />;
      break;
    case "glass-card":
      node = <GlassCard step={graphic.step} title={graphic.text} accent={accent} />;
      break;
    case "donut-stat":
      node = <DonutStat value={graphic.value ?? 100} label={graphic.label} accent={accent} />;
      break;
    case "bar-stat":
      node = <BarStat value={graphic.value ?? 50} label={graphic.label} accent={accent} />;
      break;
    case "kinetic-statement":
      node = <KineticStatement text={graphic.text} accent={accent} accent2={accent2} />;
      break;
    case "mask-reveal":
      node = <MaskReveal text={graphic.text} accent={accent} accent2={accent2} />;
      break;
    case "glass-strip":
      node = <GlassStrip text={graphic.text} accent={accent} accent2={accent2} />;
      break;
    case "path-mark":
      node = <PathMark text={graphic.text} accent={accent} kind={graphic.kind} />;
      break;
    case "shape-3d":
      node = <Shape3D text={graphic.text} accent={accent} kind={graphic.shape} />;
      break;
    case "illus-mark":
      node = <IllusMark kind={graphic.illus} accent={accent} />;
      break;
    case "step-flow":
      node = <StepFlow steps={graphic.items ?? []} accent={accent} accent2={accent2} />;
      break;
    case "comparison":
      node = <Comparison left={graphic.left ?? ""} right={graphic.right ?? ""} accent={accent} accent2={accent2} />;
      break;
    case "list-reveal":
      node = <ListReveal items={graphic.items ?? []} accent={accent} rank={graphic.rank} />;
      break;
    case "lower-third-pro":
      node = <LowerThirdPro title={graphic.text} subtitle={graphic.subtitle} accent={accent} accent2={accent2} />;
      break;
    case "info-table":
      node = <InfoTable title={graphic.text} rows={graphic.rows ?? []} accent={accent} accent2={accent2} />;
      break;
    case "stat-compare":
      node = (
        <StatCompare
          title={graphic.text}
          leftLabel={graphic.leftLabel ?? "A"}
          leftVal={graphic.leftVal ?? 0}
          rightLabel={graphic.rightLabel ?? "B"}
          rightVal={graphic.rightVal ?? 0}
          unit={graphic.unit}
          accent={accent}
          accent2={accent2}
        />
      );
      break;
    case "premium-roadmap":
      node = <PremiumRoadmap title={graphic.text} subtitle={graphic.subtitle} steps={graphic.items} rows={graphic.rows} accent={accent} />;
      break;
    case "neon-icon-card":
      node = <NeonIconCard text={graphic.text} emphasis={graphic.emphasis} icon={graphic.icon} accent={accent} />;
      break;
    case "negative-slash-card":
      node = <NegativeSlashCard text={graphic.text} accent="#EF1F2D" />;
      break;
    case "dual-icon-cards":
      node = <DualIconCards left={graphic.left} right={graphic.right} accent={accent} accent2={accent2} />;
      break;
    case "diamond-label":
      node = <DiamondLabel text={graphic.text} accent={accent} />;
      break;
    case "ad-comparison-scene":
      node = (
        <AdComparisonScene
          text={graphic.text}
          emphasis={graphic.emphasis}
          items={graphic.items}
          sourceClip={graphic.sourceClip}
          variant={graphic.adVariant}
        />
      );
      break;
    default:
      node = null;
  }
  if (!node) return null;
  // honor the EDL's anchor hint for mid-screen cards — these components place
  // themselves at a fixed height and used to ignore anchor entirely (review
  // finding: cards parked over the speaker's mouth with no way to move them)
  const ANCHOR_CARD_TYPES = new Set([
    "stat-compare", "info-table", "neon-icon-card", "negative-slash-card",
    "dual-icon-cards", "diamond-label", "list-reveal", "comparison", "step-flow",
  ]);
  const anchorShiftPct =
    graphic.anchor && ANCHOR_CARD_TYPES.has(graphic.type)
      ? { top: -26, center: -12, bottom: 0 }[graphic.anchor] ?? 0
      : 0;
  return (
    <AbsoluteFill
      style={{
        transform: `translateY(${anchorShiftPct}%) scale(${scale})`,
        transformOrigin: "50% 71%",
        pointerEvents: "none",
      }}
    >
      {node}
    </AbsoluteFill>
  );
};

/**
 * Cinematic hook — full-screen title card: darkened gradient backdrop (focus),
 * word-by-word reveal in display font with gradient emphasis, an accent underline
 * that draws in, framed by corner ticks. The 3s attention-grabber.
 */
const HookTitle: React.FC<{ text: string; accent: string; accent2: string }> = ({
  text,
  accent,
  accent2,
}) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const recipe = useStyle();
  const e = enterExit(frame, fps, durationInFrames, 8);
  const words = text.split(" ");
  const emphasisIdx = pickEmphasisIndex(words);
  const lineW = interpolate(popSpring(frame, fps, 6), [0, 1], [0, 100]);
  return (
    <AbsoluteFill style={{ opacity: e }}>
      {/* darkening + accent-tinted gradient backdrop — kept light enough that
          the speaker stays visible (0.78 made the first 3s read as a poster) */}
      <AbsoluteFill
        style={{
          background: `radial-gradient(ellipse at 50% 38%, ${accent}26, rgba(0,0,0,0.5) 72%)`,
        }}
      />
      <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", padding: 80 }}>
        <div style={{ textAlign: "center", maxWidth: 960 }}>
          <div
            style={{
              display: "flex",
              flexWrap: "wrap",
              gap: "6px 20px",
              justifyContent: "center",
              fontFamily: DISPLAY_FONT,
              fontWeight: 900,
              fontSize: 104,
              textTransform: "uppercase",
              lineHeight: VI_SAFE_LINE_HEIGHT,
              paddingTop: VI_DIACRITIC_PAD,
            }}
          >
            {words.map((w, i) => {
              const ws = popSpring(frame, fps, i * 4);
              // emphasise a content word, not whatever sits mid-sentence;
              // solid textFx = flat accent, no gradient inside a word
              const emph = i === emphasisIdx;
              return (
                <span
                  key={i}
                  style={{
                    transform: `translateY(${interpolate(ws, [0, 1], [70, 0])}px)`,
                    opacity: ws,
                    ...(emph
                      ? recipe.textFx === "solid"
                        ? { color: accent }
                        : { backgroundImage: `linear-gradient(100deg,${accent},${accent2})`, WebkitBackgroundClip: "text", backgroundClip: "text", color: "transparent" }
                      : { color: "#fff" }),
                    textShadow: emph ? "none" : "0 6px 24px rgba(0,0,0,0.6)",
                  }}
                >
                  {w}
                </span>
              );
            })}
          </div>
          {/* accent underline draws in */}
          <div
            style={{
              height: 10,
              width: `${lineW}%`,
              maxWidth: 420,
              margin: "28px auto 0",
              borderRadius: 999,
              background: `linear-gradient(90deg,${accent},${accent2})`,
              boxShadow: glow(accent, true),
            }}
          />
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

/**
 * Cinematic CTA — end card: dark backdrop, glowing gradient pill that pops + gentle
 * pulse, with an animated down-chevron prompting the follow/subscribe action.
 */
const CtaEnd: React.FC<{ text: string; accent: string; accent2: string }> = ({
  text,
  accent,
  accent2,
}) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const e = enterExit(frame, fps, durationInFrames, 8);
  const s = popSpring(frame, fps);
  const pulse = 1 + Math.sin(frame / 8) * 0.02;
  const chevron = floatY(frame, 10, 40);
  return (
    <AbsoluteFill style={{ opacity: e }}>
      <AbsoluteFill style={{ background: `radial-gradient(ellipse at 50% 55%, ${accent}33, rgba(0,0,0,0.8) 70%)` }} />
      <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", flexDirection: "column", gap: 30 }}>
        <div
          style={{
            transform: `translateY(${interpolate(s, [0, 1], [70, 0])}px) scale(${interpolate(s, [0, 1], [0.8, pulse])})`,
            background: `linear-gradient(100deg,${accent},${accent2})`,
            color: "#fff",
            fontFamily: DISPLAY_FONT,
            fontSize: 72,
            fontWeight: 900,
            padding: "30px 60px",
            borderRadius: 999,
            textAlign: "center",
            textTransform: "uppercase",
            boxShadow: glow(accent, true),
          }}
        >
          {text}
        </div>
        {/* down chevron */}
        <svg width="90" height="70" viewBox="0 0 90 70" style={{ transform: `translateY(${chevron}px)`, opacity: interpolate(s, [0, 1], [0, 1]) }}>
          <path d="M10 15 L45 50 L80 15" fill="none" stroke={accent} strokeWidth="12" strokeLinecap="round" strokeLinejoin="round" />
        </svg>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

const KineticText: React.FC<{ text: string; accent: string }> = ({ text, accent }) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const e = enterExit(frame, fps, durationInFrames);
  const words = text.split(" ");
  return (
    <AbsoluteFill style={{ ...topBandStyle(20), opacity: e }}>
      <div style={{ display: "flex", flexWrap: "wrap", gap: 12, justifyContent: "center", maxWidth: 900 }}>
        {words.map((w, i) => {
          const s = popSpring(frame, fps, i * 3);
          return (
            <span
              key={i}
              style={{
                transform: `translateY(${interpolate(s, [0, 1], [50, 0])}px) scale(${interpolate(s, [0, 1], [0.7, 1])})`,
                opacity: s,
                color: i % 2 === 0 ? "#fff" : accent,
                fontSize: 80,
                fontWeight: 900,
                textShadow: i % 2 === 0 ? "0 4px 16px rgba(0,0,0,0.6)" : glow(accent),
              }}
            >
              {w}
            </span>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};

const LowerThird: React.FC<{ text: string; accent: string }> = ({ text, accent }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const s = spring({ frame, fps, config: { damping: 14 } });
  return (
    <AbsoluteFill style={{ ...bottomBandStyle(), alignItems: "flex-start", paddingLeft: 60 }}>
      <div
        style={{
          transform: `translateX(${interpolate(s, [0, 1], [-200, 0])}px)`,
          opacity: s,
          background: accent,
          color: "#fff",
          fontSize: 44,
          fontWeight: 800,
          padding: "16px 28px",
          borderRadius: 16,
        }}
      >
        {text}
      </div>
    </AbsoluteFill>
  );
};
