/**
 * Hormozi/Karaoke-style captions — the talking-head standard.
 * 3-5 words per line, bold sans, centered, each line POPS in with a spring,
 * active word highlighted, plus one "keyword" token in the accent color.
 * Most reels are watched muted, so this caption layer is near-mandatory.
 */
import React from "react";
import {
  AbsoluteFill,
  Sequence,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import type { Caption } from "../edl-types";
import { DISPLAY_FONT, VI_SAFE_LINE_HEIGHT, VI_DIACRITIC_PAD } from "../fonts";
import { useStyle } from "../style-context";

export const Captions: React.FC<{
  captions: Caption[];
  color: string;
  highlight: string;
  accent?: string;
}> = ({ captions, color, highlight, accent = "#FF8C00" }) => {
  const { fps } = useVideoConfig();
  return (
    <AbsoluteFill>
      {captions.map((cap, i) => {
        const from = Math.round((cap.startMs / 1000) * fps);
        const end = Math.round((cap.endMs / 1000) * fps);
        const dur = Math.max(1, end - from);
        return (
          <Sequence key={i} from={from} durationInFrames={dur}>
            <CaptionLine cap={cap} color={color} highlight={highlight} accent={accent} />
          </Sequence>
        );
      })}
    </AbsoluteFill>
  );
};

const CaptionLine: React.FC<{
  cap: Caption;
  color: string;
  highlight: string;
  accent: string;
}> = ({ cap, color, highlight, accent }) => {
  const frame = useCurrentFrame();
  const { fps, height } = useVideoConfig();
  const recipe = useStyle();
  // caption band % from bottom — recipe.captionBottomPct is the FINAL value (R2-FIX2:
  // NO +3 offset; default 28 = v7's old SAFE.bottomPct 25 + 3). Higher % = sits higher.
  const paddingBottom = Math.round((height * recipe.captionBottomPct) / 100);
  const tokens = cap.tokens ?? [{ text: cap.text + " ", fromMs: cap.startMs, toMs: cap.endMs }];

  // pop-in spring at line start
  const pop = spring({ frame, fps, config: { damping: 12, mass: 0.5 } });
  const scale = interpolate(pop, [0, 1], [0.7, 1]);
  const absMs = cap.startMs + (frame / fps) * 1000;

  // auto-fit font size so long lines never overflow the safe width (~960px).
  // sizes trimmed ~8% from v7 (owner feedback: reads slightly oversized on
  // some viewers) — textScale in the recipe still scales per theme
  const charCount = tokens.reduce((n, t) => n + t.text.length, 0);
  const baseFontSize = charCount > 24 ? 56 : charCount > 16 ? 66 : 76;
  const fontSize = Math.round(baseFontSize * recipe.textScale);

  return (
    <AbsoluteFill
      style={{
        justifyContent: "flex-end",
        alignItems: "center",
        paddingBottom, // dedicated caption band, % of height (adapts 9:16 & 16:9)
      }}
    >
      <div
        style={{
          transform: `scale(${scale})`,
          display: "flex",
          flexWrap: "wrap",
          gap: 12,
          justifyContent: "center",
          alignItems: "center",
          maxWidth: 960,
          fontSize,
          fontWeight: recipe.captionCase === "sentence" ? 700 : 850,
          fontFamily: DISPLAY_FONT,
          textTransform: recipe.captionCase === "sentence" ? "none" : "uppercase",
          textAlign: "center",
          lineHeight: VI_SAFE_LINE_HEIGHT,
          paddingTop: VI_DIACRITIC_PAD,
          // slight positive tracking: -0.3 at weight 850 uppercase packed
          // letters together (owner feedback: "chữ hơi sát nhau")
          letterSpacing: recipe.captionCase === "sentence" ? 0.2 : 0.6,
        }}
      >
        {tokens.map((token, i) => {
          const isActive = token.fromMs <= absMs && token.toMs > absMs;
          const isKeyword = i === cap.keywordIdx;
          // one accent per line, not three: only the keyword carries color;
          // the spoken word pulses in SIZE, not color — a white/yellow/orange
          // dance on every line is the machine-made tell
          const c = isKeyword ? accent : color;
          return (
            <span
              key={i}
              style={{
                color: c,
                display: "inline-block",
                // 1.05 with a wider gap: 1.08 grew the active word into its
                // neighbor's gap and words visually fused ("Highlighttheo")
                transform: isActive ? "scale(1.05)" : "scale(1)",
                WebkitTextStroke: `${recipe.captionStrokePx}px rgba(0,0,0,0.7)`,
                paintOrder: "stroke fill",
                textShadow: isActive
                  ? "0 4px 18px rgba(0,0,0,0.6), 0 0 26px rgba(255,255,255,0.22)"
                  : "0 1px 3px rgba(0,0,0,0.55), 0 4px 14px rgba(0,0,0,0.48)",
              }}
            >
              {token.text.trim()}
            </span>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};
