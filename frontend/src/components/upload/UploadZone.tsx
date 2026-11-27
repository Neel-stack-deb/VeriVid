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
      className={`relative rounded-2xl border-2 border-dashed p-10 text-center transition-colors ${
        dragging
          ? "border-violet-400 bg-violet-500/5"
          : "border-zinc-700 bg-[#0e0f14]"
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
        onChange={(e) => {
          const file = e.target.files?.[0];
          if (file) void handleFile(file);
        }}
      />
      <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-xl bg-violet-500/10 text-violet-300">
        {uploading ? (
          <FileVideo className="h-7 w-7 animate-pulse" aria-hidden />
        ) : (
          <Upload className="h-7 w-7" aria-hidden />
        )}
      </div>
      <p className="mt-4 text-lg font-medium text-zinc-100">
        Drop a video or browse files
      </p>
      <p className="mt-2 text-sm text-zinc-500">
        MP4, MOV, AVI, MKV, WEBM — up to 500 MB
      </p>
      {progress !== null ? (
        <div className="mx-auto mt-6 max-w-xs">
          <div className="h-1.5 overflow-hidden rounded-full bg-zinc-800">
            <div
              className="h-full bg-violet-500 transition-all"
              style={{ width: `${Math.round(progress * 100)}%` }}
            />
          </div>
        </div>
      ) : null}
      {error ? (
        <p className="mt-4 text-sm text-rose-400" role="alert">
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