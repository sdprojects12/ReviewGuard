const STAMP_CONFIG = {
  approve: {
    label: "Approved",
    color: "var(--color-approve)",
    rotate: "-6deg",
  },
  needs_adjustment: {
    label: "Needs Adjustment",
    color: "var(--color-adjust)",
    rotate: "-3deg",
  },
  reject: {
    label: "Rejected",
    color: "var(--color-reject)",
    rotate: "-8deg",
  },
};

/**
 * DecisionStamp — the moderation decision rendered as a stamped mark,
 * not a colored pill. This is ReviewGuard's signature visual element.
 *
 * @param {{ decision: "approve" | "needs_adjustment" | "reject" }} props
 */
export default function DecisionStamp({ decision }) {
  const config = STAMP_CONFIG[decision];
  if (!config) return null;

  return (
    <div
      className="stamp-animate inline-block select-none"
      style={{ "--stamp-rotate": config.rotate }}
    >
      <div
        className="px-5 py-2.5 border-4 rounded-sm font-display text-xl md:text-2xl tracking-widest uppercase"
        style={{
          color: config.color,
          borderColor: config.color,
          boxShadow: `inset 0 0 0 2px ${config.color}`,
        }}
      >
        {config.label}
      </div>
    </div>
  );
}