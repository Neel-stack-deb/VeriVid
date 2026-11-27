import { VideoWorkspaceClient } from "@/components/video/VideoWorkspaceClient";

export default async function VideoPage({
  params,
}: {
  params: Promise<{ videoId: string }>;
}) {
  const { videoId } = await params;
  return <VideoWorkspaceClient videoId={videoId} />;
}