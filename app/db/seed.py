import logging
from datetime import datetime, timedelta

from app.core.security import hash_password
from app.db.session import SessionLocal
from app.models.comment import Comment
from app.models.project import Project
from app.models.project_member import ProjectMember
from app.models.task import Task
from app.models.user import User

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def seed_database() -> None:
    db = SessionLocal()
    try:
        logger.info("🌱 Starting database seeding process...")

        # ---------------------------------------------------------
        # 1. Seed Users
        # ---------------------------------------------------------
        users_data = [
            {
                "firstname": "System",
                "lastname": "Admin",
                "email": "admin@example.com",
                "password": "AdminPassword123!",
                "role": "admin",
                "is_active": True,
            },
            {
                "firstname": "Project",
                "lastname": "Manager",
                "email": "manager@example.com",
                "password": "ManagerPassword123!",
                "role": "manager",
                "is_active": True,
            },
            {
                "firstname": "Alex",
                "lastname": "Developer",
                "email": "developer@example.com",
                "password": "DeveloperPassword123!",
                "role": "user",
                "is_active": True,
            },
            {
                "firstname": "Bob",
                "lastname": "UserB",
                "email": "user_b@example.com",
                "password": "UserBPassword123!",
                "role": "user",
                "is_active": True,
            },
        ]

        user_map: dict[str, User] = {}
        for u in users_data:
            existing_user = db.query(User).filter(User.email == u["email"]).first()
            if not existing_user:
                user = User(
                    firstname=u["firstname"],
                    lastname=u["lastname"],
                    email=u["email"],
                    password_hash=hash_password(u["password"]),
                    role=u["role"],
                    is_active=u["is_active"],
                )
                db.add(user)
                db.flush()
                user_map[u["email"]] = user
                logger.info("  [+] Created User: %s (%s)", u["email"], u["role"])
            else:
                user_map[u["email"]] = existing_user
                logger.info("  [~] User already exists: %s", u["email"])

        manager_user = user_map["manager@example.com"]
        dev_user = user_map["developer@example.com"]
        user_b = user_map["user_b@example.com"]

        # ---------------------------------------------------------
        # 2. Seed Projects
        # ---------------------------------------------------------
        projects_data = [
            {
                "name": "Cloud Infrastructure Migration",
                "client_name": "Acme Global Tech",
                "description": "Multi-region migration of microservices to Kubernetes clusters with zero downtime.",
                "status": "active",
                "start_date": datetime.utcnow() - timedelta(days=30),
                "end_date": datetime.utcnow() + timedelta(days=60),
            },
            {
                "name": "Mobile Banking Redesign",
                "client_name": "Horizon Financial",
                "description": "Next-generation iOS & Android application featuring biometric auth and instant transfers.",
                "status": "active",
                "start_date": datetime.utcnow() - timedelta(days=15),
                "end_date": datetime.utcnow() + timedelta(days=90),
            },
            {
                "name": "Confidential Security Audit",
                "client_name": "Internal Corp",
                "description": "Internal security assessment and penetration testing (Private to User B).",
                "status": "active",
                "start_date": datetime.utcnow() - timedelta(days=5),
                "end_date": datetime.utcnow() + timedelta(days=20),
            },
        ]

        project_map: dict[str, Project] = {}
        for p in projects_data:
            existing_project = db.query(Project).filter(Project.name == p["name"]).first()
            if not existing_project:
                project = Project(
                    name=p["name"],
                    client_name=p["client_name"],
                    description=p["description"],
                    status=p["status"],
                    start_date=p["start_date"],
                    end_date=p["end_date"],
                )
                db.add(project)
                db.flush()
                project_map[p["name"]] = project
                logger.info("  [+] Created Project: %s", p["name"])
            else:
                project_map[p["name"]] = existing_project
                logger.info("  [~] Project already exists: %s", p["name"])

        p_cloud = project_map["Cloud Infrastructure Migration"]
        p_mobile = project_map["Mobile Banking Redesign"]
        p_audit = project_map["Confidential Security Audit"]

        # ---------------------------------------------------------
        # 3. Seed Project Members
        # ---------------------------------------------------------
        members_data = [
            # Cloud Migration: Manager (PROJECT_MANAGER), Dev (MEMBER)
            {"project_id": p_cloud.id, "user_id": manager_user.id, "role": "PROJECT_MANAGER"},
            {"project_id": p_cloud.id, "user_id": dev_user.id, "role": "MEMBER"},
            # Mobile Redesign: Manager (PROJECT_MANAGER)
            {"project_id": p_mobile.id, "user_id": manager_user.id, "role": "PROJECT_MANAGER"},
            # Security Audit: User B (PROJECT_MANAGER) - isolated for BOLA test
            {"project_id": p_audit.id, "user_id": user_b.id, "role": "PROJECT_MANAGER"},
        ]

        for m in members_data:
            existing_pm = (
                db.query(ProjectMember)
                .filter(
                    ProjectMember.project_id == m["project_id"],
                    ProjectMember.user_id == m["user_id"],
                )
                .first()
            )
            if not existing_pm:
                pm = ProjectMember(
                    project_id=m["project_id"],
                    user_id=m["user_id"],
                    project_role=m["role"],
                    joined_at=datetime.utcnow(),
                )
                db.add(pm)
                logger.info("  [+] Added User ID %d to Project ID %d as %s", m["user_id"], m["project_id"], m["role"])

        db.flush()

        # ---------------------------------------------------------
        # 4. Seed Tasks
        # ---------------------------------------------------------
        tasks_data = [
            {
                "project_id": p_cloud.id,
                "title": "Setup Terraform CI/CD Modules",
                "description": "Automate VPC, subnets, and security groups provisioning via GitHub Actions.",
                "status": "completed",
                "priority": "high",
                "assigned_to_user_id": dev_user.id,
                "due_date": datetime.utcnow() + timedelta(days=5),
            },
            {
                "project_id": p_cloud.id,
                "title": "Configure Redis Caching & Rate Limiter",
                "description": "Deploy Redis instance and connect authentication rate limiters to mitigate brute force.",
                "status": "in_progress",
                "priority": "urgent",
                "assigned_to_user_id": dev_user.id,
                "due_date": datetime.utcnow() + timedelta(days=7),
            },
            {
                "project_id": p_cloud.id,
                "title": "Implement Database Auto-Scaling Policies",
                "description": "Configure RDS Read Replicas and alarm thresholds.",
                "status": "pending",
                "priority": "medium",
                "assigned_to_user_id": manager_user.id,
                "due_date": datetime.utcnow() + timedelta(days=14),
            },
            {
                "project_id": p_mobile.id,
                "title": "Figma Wireframes Approval",
                "description": "Complete UI/UX review with client stakeholders.",
                "status": "in_progress",
                "priority": "high",
                "assigned_to_user_id": manager_user.id,
                "due_date": datetime.utcnow() + timedelta(days=10),
            },
            {
                "project_id": p_audit.id,
                "title": "Conduct Threat Modeling Session",
                "description": "Identify architectural threat vectors and privilege boundaries.",
                "status": "pending",
                "priority": "high",
                "assigned_to_user_id": user_b.id,
                "due_date": datetime.utcnow() + timedelta(days=3),
            },
        ]

        task_map: dict[str, Task] = {}
        for t in tasks_data:
            existing_task = (
                db.query(Task)
                .filter(Task.project_id == t["project_id"], Task.title == t["title"])
                .first()
            )
            if not existing_task:
                task = Task(
                    project_id=t["project_id"],
                    title=t["title"],
                    description=t["description"],
                    status=t["status"],
                    priority=t["priority"],
                    assigned_to_user_id=t["assigned_to_user_id"],
                    due_date=t["due_date"],
                )
                db.add(task)
                db.flush()
                task_map[t["title"]] = task
                logger.info("  [+] Created Task: '%s' (Project ID: %d)", t["title"], t["project_id"])
            else:
                task_map[t["title"]] = existing_task

        # ---------------------------------------------------------
        # 5. Seed Comments
        # ---------------------------------------------------------
        comments_data = [
            {
                "task_title": "Setup Terraform CI/CD Modules",
                "user_id": dev_user.id,
                "comment": "Terraform code has been merged and staging plan validated successfully.",
            },
            {
                "task_title": "Setup Terraform CI/CD Modules",
                "user_id": manager_user.id,
                "comment": "Great work Alex! Production rollout scheduled for Friday night.",
            },
            {
                "task_title": "Configure Redis Caching & Rate Limiter",
                "user_id": dev_user.id,
                "comment": "Redis cluster configured on port 6379 with auth enabled.",
            },
            {
                "task_title": "Conduct Threat Modeling Session",
                "user_id": user_b.id,
                "comment": "Initial STRIDE analysis completed. Preparing report.",
            },
        ]

        for c in comments_data:
            target_task = task_map.get(c["task_title"])
            if target_task:
                existing_comment = (
                    db.query(Comment)
                    .filter(
                        Comment.task_id == target_task.id,
                        Comment.user_id == c["user_id"],
                        Comment.comment == c["comment"],
                    )
                    .first()
                )
                if not existing_comment:
                    comment = Comment(
                        task_id=target_task.id,
                        user_id=c["user_id"],
                        comment=c["comment"],
                        created_at=datetime.utcnow(),
                    )
                    db.add(comment)
                    logger.info("  [+] Added Comment to Task '%s' by User ID %d", c["task_title"], c["user_id"])

        db.commit()
        logger.info("✅ Database successfully seeded!")
        logger.info("===============================================================")
        logger.info("🔑 Seeded Demonstration Credentials:")
        logger.info("   1. Admin:     admin@example.com     / AdminPassword123!")
        logger.info("   2. Manager:   manager@example.com   / ManagerPassword123!")
        logger.info("   3. Developer: developer@example.com / DeveloperPassword123!")
        logger.info("   4. User B:    user_b@example.com    / UserBPassword123!")
        logger.info("===============================================================")

    except Exception as exc:
        db.rollback()
        logger.error("❌ Seeding failed: %s", exc)
        raise exc
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
