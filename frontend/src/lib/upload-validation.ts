import { ALLOWED_EXTENSIONS } from "@/lib/constants";

const MAX_BYTES = 500 * 1024 * 1024;

export function validateVideoFile(file: File): string | null {
  const name = file.name.toLowerCase();
  const ext = ALLOWED_EXTENSIONS.find((allowed) => name.endsWith(allowed));
  if (!ext) {
    return `Unsupported format. Allowed: ${ALLOWED_EXTENSIONS.join(", ")}`;
  }
  if (file.size > MAX_BYTES) {
    return "File exceeds the 500 MB upload limit.";
  }
  if (file.size === 0) {
    return "File is empty.";
  }
  return null;
}