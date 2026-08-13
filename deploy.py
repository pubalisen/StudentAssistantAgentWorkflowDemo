"""Deploy UCSC Student Services Agent to Vertex AI Agent Engine.

Usage (from GCP Cloud Shell):
    # First time: authenticate and create staging bucket
    gcloud auth application-default login
    gsutil mb -l us-central1 gs://YOUR_PROJECT-adk-staging

    # Deploy
    python deploy.py
    python deploy.py --project mygenerativeai
    python deploy.py --dry-run
"""

import argparse
import os
import sys

from dotenv import load_dotenv
load_dotenv("app/.env")


def main():
    parser = argparse.ArgumentParser(description="Deploy agent to Vertex AI Agent Engine")
    parser.add_argument("--project", default=os.environ.get("GOOGLE_CLOUD_PROJECT", "mygenerativeai"))
    parser.add_argument("--region", default=os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1"))
    parser.add_argument("--staging-bucket", default=None, help="GCS bucket for staging (e.g. gs://my-bucket)")
    parser.add_argument("--dry-run", action="store_true", help="Validate without deploying")
    parser.add_argument("--display-name", default="UCSC Student Services Agent")
    parser.add_argument("--list", action="store_true", help="List existing deployed agents")
    args = parser.parse_args()

    print(f"╔══════════════════════════════════════════════════════════════╗")
    print(f"║       UCSC Student Services — Deploy to Agent Engine        ║")
    print(f"╚══════════════════════════════════════════════════════════════╝")
    print()
    print(f"  Project:  {args.project}")
    print(f"  Region:   {args.region}")
    print(f"  Agent:    {args.display_name}")
    print()

    # ── Step 1: Validate agent import ────────────────────────
    print("📦 Step 1: Validating agent structure...")
    try:
        from app.agent import root_agent
        print(f"   ✅ Root agent: {root_agent.name}")
        print(f"   ✅ Model: {root_agent.model}")
        sub_agents = root_agent.sub_agents or []
        print(f"   ✅ Sub-agents ({len(sub_agents)}):")
        for sa in sub_agents:
            agent_type = type(sa).__name__
            sub_count = len(sa.sub_agents) if hasattr(sa, 'sub_agents') and sa.sub_agents else 0
            print(f"       • {sa.name} ({agent_type}) — {sub_count} sub-agents")
        print(f"   ✅ Tools: {len(root_agent.tools)} toolset(s)")
    except Exception as e:
        print(f"   ❌ Import failed: {e}")
        sys.exit(1)

    if args.dry_run:
        print("\n🧪 Dry run complete — agent is valid and ready to deploy.")
        return

    # ── Step 2: Check authentication ─────────────────────────
    print("\n🔐 Step 2: Checking authentication...")
    try:
        import google.auth
        credentials, project = google.auth.default()
        print(f"   ✅ Authenticated as: {getattr(credentials, 'service_account_email', 'user')}")
        print(f"   ✅ Project: {project or args.project}")
    except Exception as e:
        print(f"   ❌ Auth failed: {e}")
        print("   Run: gcloud auth application-default login")
        sys.exit(1)

    # ── Step 3: List existing agents (optional) ──────────────
    if args.list:
        print("\n📋 Step 3: Listing existing agents...")
        try:
            from google.cloud import aiplatform
            aiplatform.init(project=args.project, location=args.region)
            from vertexai import agent_engines
            existing = agent_engines.list()
            if existing:
                for eng in existing:
                    print(f"   • {eng.display_name} (resource: {eng.resource_name})")
            else:
                print("   No agents deployed yet.")
        except Exception as e:
            print(f"   ⚠️ Could not list agents: {e}")
        return

    # ── Step 4: Deploy ───────────────────────────────────────
    print("\n🚀 Step 4: Deploying to Agent Engine...")
    try:
        from google.cloud import aiplatform
        aiplatform.init(project=args.project, location=args.region)

        from vertexai import agent_engines

        staging_bucket = args.staging_bucket
        if not staging_bucket:
            staging_bucket = f"gs://{args.project}-adk-staging"
            print(f"   Using staging bucket: {staging_bucket}")

        remote_agent = agent_engines.create(
            agent_engine=root_agent,
            requirements=[
                "google-adk>=1.3.0",
                "google-cloud-aiplatform>=1.60.0",
                "python-dotenv>=1.0.0",
            ],
            display_name=args.display_name,
            staging_bucket=staging_bucket,
        )

        print(f"\n   ✅ Deployed successfully!")
        print(f"   Resource: {remote_agent.resource_name}")
        print(f"   Display Name: {remote_agent.display_name}")

    except Exception as e:
        print(f"   ❌ Deployment failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
