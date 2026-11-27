import { VideoAnalysisClient } from "@/components/video/VideoAnalysisClient";

export default async function VideoAnalysisPage({
  params,
}: {
  params: Promise<{ videoId: string }>;
}) {
  const { videoId } = await params;
  return <VideoAnalysisClient videoId={videoId} />;
}