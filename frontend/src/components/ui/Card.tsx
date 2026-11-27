import type { HTMLAttributes, ReactNode } from "react";

export function Card({
  children,
  className = "",
  hover = false,
  ...props
}: HTMLAttributes<HTMLDivElement> & { children: ReactNode; hover?: boolean }) {
  return (
    <div
      className={`rounded-[var(--radius-lg)] border border-[var(--border-default)] bg-[var(--bg-elevated)] shadow-[var(--shadow-card)] ${
        hover
          ? "transition-colors hover:border-zinc-600 hover:bg-[var(--bg-hover)]"
          : ""
      } ${className}`}
      {...props}
    >
      {children}
    </div>
  );
}

export function CardHeader({
  title,
  description,
  action,
}: {
  title: string;
  description?: string;
  action?: ReactNode;
}) {
  return (
    <div className="flex items-start justify-between gap-4 border-b border-[var(--border-subtle)] px-5 py-4">
      <div>
        <h3 className="text-sm font-medium text-[var(--text-primary)]">{title}</h3>
        {description ? (
          <p className="mt-1 text-xs text-[var(--text-muted)]">{description}</p>
        ) : null}
      </div>
      {action}
    </div>
  );
}