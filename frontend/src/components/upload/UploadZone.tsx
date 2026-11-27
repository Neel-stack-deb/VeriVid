"use client";

import { useCallback, useRef, useState } from "react";
import { Upload, FileVideo } from "lucide-react";

import { uploadVideo } from "@/lib/api/client";
import { saveRecentVideo } from "@/lib/recent-videos";
import { validateVideoFile } from "@/lib/upload-validation";
import { Button } from "@/components/ui/Button";

export function UploadZone({
  onUploaded,
}: {
  onUploaded: (videoId: string, filename: string) => void;
}) {
  const inputRef = useRef<HTMLInputElement>(null);
  const [dragging, setDragging] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [progress, setProgress] = useState<number | null>(null);
  const [uploading, setUploading] = useState(false);

  const handleFile = useCallback(
    async (file: File) => {
      const validation = validateVideoFile(file);
      if (validation) {
        setError(validation);
        return;
      }
      setError(null);
      setUploading(true);
      setProgress(0);
      try {
        const result = await uploadVideo(file, setProgress);
        saveRecentVideo({
          videoId: result.video_id,
          filename: result.filename,
          addedAt: new Date().toISOString(),
        });
        onUploaded(result.video_id, result.filename);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Upload failed");
      } finally {
        setUploading(false);
        setProgress(null);
      }
    },
    [onUploaded],
  );

  const onDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault();
      setDragging(false);
      const file = e.dataTransfer.files[0];
      if (file) void handleFile(file);
    },
    [handleFile],
  );

  return (
    <div
      className={`relative rounded-[var(--radius-xl)] border-2 border-dashed p-8 text-center transition-colors sm:p-10 ${
        dragging
          ? "border-violet-400 bg-[var(--accent-muted)]"
          : "border-[var(--border-default)] bg-[var(--bg-muted)]"
      }`}
      onDragOver={(e) => {
        e.preventDefault();
        setDragging(true);
      }}
      onDragLeave={() => setDragging(false)}
      onDrop={onDrop}
    >
      <input
        ref={inputRef}
        type="file"
        accept=".mp4,.mov,.avi,.mkv,.webm,video/*"
        className="hidden"
        aria-label="Choose video file"
        onChange={(e) => {
          const file = e.target.files?.[0];
          if (file) void handleFile(file);
        }}
      />
      <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-[var(--radius-lg)] border border-violet-500/25 bg-[var(--accent-muted)] text-violet-300">
        {uploading ? (
          <FileVideo className="h-6 w-6 animate-pulse" aria-hidden />
        ) : (
          <Upload className="h-6 w-6" aria-hidden />
        )}
      </div>
      <p className="mt-4 text-base font-medium text-[var(--text-primary)]">
        Drop a video or browse files
      </p>
      <p className="mt-2 text-sm text-[var(--text-muted)]">
        MP4, MOV, AVI, MKV, WEBM — up to 500 MB
      </p>
      {progress !== null ? (
        <div className="mx-auto mt-6 max-w-xs">
          <div
            className="h-1 overflow-hidden rounded-full bg-[var(--bg-hover)]"
            role="progressbar"
            aria-valuenow={Math.round(progress * 100)}
            aria-valuemin={0}
            aria-valuemax={100}
          >
            <div
              className="h-full bg-[var(--accent)] transition-[width]"
              style={{ width: `${Math.round(progress * 100)}%` }}
            />
          </div>
          <p className="mt-2 text-xs text-[var(--text-muted)]">
            Uploading… {Math.round(progress * 100)}%
          </p>
        </div>
      ) : null}
      {error ? (
        <p className="mt-4 text-sm text-[var(--error)]" role="alert">
          {error}
        </p>
      ) : null}
      <div className="mt-6">
        <Button
          type="button"
          variant="secondary"
          disabled={uploading}
          onClick={() => inputRef.current?.click()}
        >
          Choose video
        </Button>
      </div>
    </div>
  );
}