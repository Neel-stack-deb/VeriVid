import json

from app.schemas.debate.debate_artifacts import DebateArtifacts
from app.schemas.video_workspace import VideoWorkspace


class DebatePersistenceService:

    @staticmethod
    def save(
        workspace: VideoWorkspace,
        artifacts: DebateArtifacts,
    ) -> None:

        debate_dir = workspace.debate_dir

        files = {
            "context.json": artifacts.context_report,
            "verification.json": artifacts.verification_report,
            "risk.json": artifacts.risk_report,
            "consensus.json": artifacts.consensus_report,
        }

        for filename, report in files.items():
            if report is None:
                continue

            with open(
                debate_dir / filename,
                "w",
                encoding="utf-8",
            ) as file:

                json.dump(
                    report.model_dump(),
                    file,
                    indent=2,
                    ensure_ascii=False,
                )