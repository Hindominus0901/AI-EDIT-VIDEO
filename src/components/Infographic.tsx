/**
 * Designed infographic components — structured motion-graphics that VISUALIZE
 * content (steps, lists, comparisons, stats), the way a motion designer composes
 * them: multi-element, layered, staggered reveal, gradient + depth. Pure React/CSS,
 * theme-colored. This is "graphics design", not single-stroke vector.
 */
import React from "react";
import {
  AbsoluteFill,
  interpolate,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { enterExit, voicePop, grammar, glow } from "../anim";
import { useStyle } from "../style-context";
import { DISPLAY_FONT, BODY_FONT } from "../fonts";

const grad = (a: string, b: string) => `linear-gradient(120deg, ${a}, ${b})`;

/**
 * Stage wrapper for big infographics — places content in the CENTER (where the eye
 * looks) and dims/blurs the video behind it so the graphic reads clearly, like a
 * pro editor's "focus card". The scrim fades with the graphic's enter/exit.
 */
const InfoStage: React.FC<{ e: number; children: React.ReactNode; align?: "center" | "flex-start" }> = ({
  e,
  children,
  align = "center",
}) => (
  <AbsoluteFill style={{ opacity: e }}>
    <AbsoluteFill style={{ background: "rgba(0,0,0,0.45)", backdropFilter: "blur(6px)" }} />
    <AbsoluteFill style={{ alignItems: align, justifyContent: "center", paddingLeft: align === "flex-start" ? 90 : 0 }}>
      {children}
    </AbsoluteFill>
  </AbsoluteFill>
);

/** Numbered step flow (1→2→3) — staggered cards with connecting flow. */
export const StepFlow: React.FC<{ steps: string[]; accent: string; accent2: string }> = ({
  steps,
  accent,
  accent2,
}) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const recipe = useStyle();
  // GAP B: data grammar — step flows are structured data
  const g = grammar("data", frame, fps, durationInFrames);
  const e = g.opacity;
  const items = steps.slice(0, 4);
  return (
    <InfoStage e={e}>
      <div style={{ display: "flex", flexDirection: "column", gap: 18, width: 880 }}>
        {items.map((s, i) => {
          const sp = voicePop(frame, fps, recipe.motionVoice, i * 6);
          return (
            <div
              key={i}
              style={{
                display: "flex",
                alignItems: "center",
                gap: 22,
                transform: `translateX(${interpolate(sp, [0, 1], [-120, 0])}px)`,
                opacity: sp,
                background: "rgba(255,255,255,0.10)",
                backdropFilter: "blur(14px)",
                border: "1px solid rgba(255,255,255,0.25)",
                borderRadius: 22,
                padding: "18px 26px",
                boxShadow: glow(accent),
              }}
            >
              <div style={{ minWidth: 72, height: 72, borderRadius: 18, background: grad(accent, accent2),
                display: "flex", alignItems: "center", justifyContent: "center",
                fontFamily: DISPLAY_FONT, fontSize: 44, fontWeight: 900, color: "#fff" }}>
                {i + 1}
              </div>
              <div style={{ fontFamily: BODY_FONT, fontSize: 40, fontWeight: 700, color: "#fff" }}>{s}</div>
            </div>
          );
        })}
      </div>
    </InfoStage>
  );
};

/** Two-column comparison (vs) — left/right cards slide in from sides. */
export const Comparison: React.FC<{ left: string; right: string; accent: string; accent2: string }> = ({
  left,
  right,
  accent,
  accent2,
}) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const recipe = useStyle();
  const gm = grammar("data", frame, fps, durationInFrames);
  const e = gm.opacity;
  const sp = voicePop(frame, fps, recipe.motionVoice);
  const card = (txt: string, c: string, from: number, label: string) => (
    <div style={{ flex: 1, transform: `translateX(${interpolate(sp, [0, 1], [from, 0])}px)`,
      background: "rgba(255,255,255,0.10)", backdropFilter: "blur(14px)",
      border: `2px solid ${c}`, borderRadius: 22, padding: "26px 20px", textAlign: "center" }}>
      <div style={{ fontFamily: DISPLAY_FONT, fontSize: 28, fontWeight: 900, color: c, textTransform: "uppercase", marginBottom: 10 }}>{label}</div>
      <div style={{ fontFamily: BODY_FONT, fontSize: 38, fontWeight: 700, color: "#fff" }}>{txt}</div>
    </div>
  );
  return (
    <InfoStage e={e}>
      <div style={{ display: "flex", gap: 16, width: 920, alignItems: "stretch", position: "relative" }}>
        {card(left, accent, -200, "Trước")}
        <div style={{ alignSelf: "center", fontFamily: DISPLAY_FONT, fontSize: 48, fontWeight: 900,
          color: "#fff", transform: `scale(${sp})` }}>VS</div>
        {card(right, accent2, 200, "Sau")}
      </div>
    </InfoStage>
  );
};

/** Bulleted list reveal — items pop one by one with accent bullets. */
export const ListReveal: React.FC<{ items: string[]; accent: string; rank?: number }> = ({ items, accent, rank }) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const recipe = useStyle();
  const g = grammar("data", frame, fps, durationInFrames);
  const e = g.opacity;
  return (
    <InfoStage e={e} align="flex-start">
      <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
        {items.slice(0, 4).map((s, i) => {
          const sp = voicePop(frame, fps, recipe.motionVoice, i * 7);
          // GROUP 1 priority: highlight the top-ranked item (bigger + glow)
          const isTop = rank != null && i === rank - 1;
          return (
            <div key={i} style={{ display: "flex", alignItems: "center", gap: 18,
              transform: `translateX(${interpolate(sp, [0, 1], [-80, 0])}px)`, opacity: sp }}>
              <div style={{ width: isTop ? 34 : 26, height: isTop ? 34 : 26, borderRadius: 8,
                background: accent, boxShadow: glow(accent, isTop), transform: "rotate(45deg)" }} />
              <span style={{ fontFamily: DISPLAY_FONT, fontSize: isTop ? 56 : 48, fontWeight: isTop ? 900 : 800,
                color: "#fff", textShadow: "0 4px 14px rgba(0,0,0,0.6)" }}>{s}</span>
            </div>
          );
        })}
      </div>
    </InfoStage>
  );
};

/** Pro lower-third — designed name/label bar (multi-layer, accent block + text). */
export const LowerThirdPro: React.FC<{ title: string; subtitle?: string; accent: string; accent2: string }> = ({
  title,
  subtitle,
  accent,
  accent2,
}) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames, height } = useVideoConfig();
  const recipe = useStyle();
  const e = enterExit(frame, fps, durationInFrames, 12);
  const sp = voicePop(frame, fps, recipe.motionVoice);
  const w = interpolate(sp, [0, 1], [0, 100]);
  // sit ABOVE caption band (which is at ~28%) so the two don't collide / hit UI
  const padBottom = Math.round(height * 0.36);
  return (
    <AbsoluteFill style={{ alignItems: "flex-start", justifyContent: "flex-end", paddingBottom: padBottom, paddingLeft: 70, opacity: e }}>
      <div style={{ position: "relative" }}>
        {/* accent block grows in */}
        <div style={{ position: "absolute", left: 0, top: 0, bottom: 0, width: 14, background: grad(accent, accent2), borderRadius: 8 }} />
        <div style={{ overflow: "hidden", width: `${w}%` }}>
          <div style={{ background: "rgba(0,0,0,0.6)", backdropFilter: "blur(10px)", padding: "14px 30px 14px 34px", borderRadius: "0 14px 14px 0", whiteSpace: "nowrap" }}>
            <div style={{ fontFamily: DISPLAY_FONT, fontSize: 50, fontWeight: 900, color: "#fff", textTransform: "uppercase" }}>{title}</div>
            {subtitle ? <div style={{ fontFamily: BODY_FONT, fontSize: 30, fontWeight: 600, color: accent }}>{subtitle}</div> : null}
          </div>
        </div>
      </div>
    </AbsoluteFill>
  );
};
