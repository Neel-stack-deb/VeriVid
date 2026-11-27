import type { ButtonHTMLAttributes } from "react";

const variants = {
  primary:
    "bg-violet-600 text-white hover:bg-violet-500 border border-violet-500/50 shadow-[0_0_0_1px_rgba(139,92,246,0.2)]",
  secondary:
    "bg-[#1a1a22] text-zinc-200 border border-zinc-700 hover:border-zinc-500 hover:bg-[#22222c]",
  ghost: "text-zinc-300 hover:text-white hover:bg-white/5",
};

type Variant = keyof typeof variants;

export function Button({
  variant = "primary",
  className = "",
  ...props
}: ButtonHTMLAttributes<HTMLButtonElement> & { variant?: Variant }) {
  return (
    <button
      className={`inline-flex items-center justify-center gap-2 rounded-lg px-4 py-2.5 text-sm font-medium transition-colors focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-violet-400 disabled:opacity-50 disabled:pointer-events-none ${variants[variant]} ${className}`}
      {...props}
    />
  );
}