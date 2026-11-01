
from mcp.server.fastmcp import FastMCP
from sqlalchemy import select
import json

from database import Base, engine, SessionLocal
from models import UserProfile
from schemas import UserProfileCreate, UserProfileUpdate


# ============================================================
# CREATE MCP SERVER
# ============================================================

mcp = FastMCP("User Memory Server")


# ============================================================
# CREATE DATABASE TABLE
# ============================================================

Base.metadata.create_all(bind=engine)


# ============================================================
# SAVE NEW PROFILE
# ============================================================

@mcp.tool()
def save_profile(profile: UserProfileCreate) -> str:
    """
    Save a new profile.
    Every call creates a new database row.
    Existing profiles are not deleted or overwritten.
    """

    db = SessionLocal()

    try:
        user = UserProfile(
            name=profile.name,
            age=profile.age,
            mobile=profile.mobile,
            location=profile.location
        )

        db.add(user)

        db.commit()

        db.refresh(user)

        return (
            f"Profile saved successfully.\n"
            f"Profile ID: {user.id}\n"
            f"Name: {user.name}"
        )

    except Exception as e:
        db.rollback()
        return f"Error saving profile: {str(e)}"

    finally:
        db.close()


# ============================================================
# GET ONE PROFILE BY ID
# ============================================================

@mcp.tool()
def get_profile(profile_id: int) -> str:
    """
    Get one specific profile using its ID.
    """

    db = SessionLocal()

    try:
        user = db.execute(
            select(UserProfile).where(
                UserProfile.id == profile_id
            )
        ).scalar_one_or_none()

        if user is None:
            return json.dumps(
                {
                    "message": f"No profile found with ID {profile_id}."
                },
                indent=2
            )

        profile = {
            "id": user.id,
            "name": user.name,
            "age": user.age,
            "mobile": user.mobile,
            "location": user.location
        }

        return json.dumps(
            profile,
            indent=2
        )

    finally:
        db.close()


# ============================================================
# GET ALL PROFILES
# ============================================================

@mcp.tool()
def get_all_profiles() -> str:
    """
    Get ALL saved profiles from the SQLite database.
    """

    db = SessionLocal()

    try:

        # ----------------------------------------------------
        # GET EVERY ROW FROM THE TABLE
        # ----------------------------------------------------

        users = db.execute(
            select(UserProfile).order_by(
                UserProfile.id
            )
        ).scalars().all()


        # ----------------------------------------------------
        # PRINT COUNT IN SERVER TERMINAL
        # ----------------------------------------------------

        print(
            f"\n[GET ALL PROFILES] "
            f"Database contains {len(users)} profile(s)."
        )


        # ----------------------------------------------------
        # DATABASE EMPTY
        # ----------------------------------------------------

        if not users:

            return json.dumps(
                {
                    "message": "No profiles found."
                },
                indent=2
            )


        # ----------------------------------------------------
        # CREATE LIST OF ALL PROFILES
        # ----------------------------------------------------

        profiles = []

        for user in users:

            profiles.append(
                {
                    "id": user.id,
                    "name": user.name,
                    "age": user.age,
                    "mobile": user.mobile,
                    "location": user.location
                }
            )


        # ----------------------------------------------------
        # PRINT PROFILES IN SERVER TERMINAL
        # ----------------------------------------------------

        print(
            f"[GET ALL PROFILES] "
            f"Returning {len(profiles)} profile(s)."
        )


        # ----------------------------------------------------
        # RETURN ALL PROFILES
        # ----------------------------------------------------

        return json.dumps(
            profiles,
            indent=2
        )

    except Exception as e:

        print(
            f"[GET ALL PROFILES ERROR] {str(e)}"
        )

        return json.dumps(
            {
                "error": str(e)
            },
            indent=2
        )

    finally:

        db.close()


# ============================================================
# UPDATE PROFILE
# ============================================================

@mcp.tool()
def update_profile(
    profile_id: int,
    profile: UserProfileUpdate
) -> str:
    """
    Update a specific profile using its ID.
    """

    db = SessionLocal()

    try:

        user = db.execute(
            select(UserProfile).where(
                UserProfile.id == profile_id
            )
        ).scalar_one_or_none()

        if user is None:

            return (
                f"No profile found with ID {profile_id}."
            )


        # Update only fields that were provided

        if profile.name is not None:
            user.name = profile.name

        if profile.age is not None:
            user.age = profile.age

        if profile.mobile is not None:
            user.mobile = profile.mobile

        if profile.location is not None:
            user.location = profile.location


        db.commit()


        return (
            f"Profile ID {profile_id} "
            f"updated successfully."
        )

    except Exception as e:

        db.rollback()

        return f"Error updating profile: {str(e)}"

    finally:

        db.close()


# ============================================================
# START MCP SERVER
# ============================================================

if __name__ == "__main__":

    print(
        "=========================================="
    )

    print(
        "       USER MEMORY MCP SERVER"
    )

    print(
        "=========================================="
    )

    print(
        "Database: user_profile.db"
    )

    print(
        "HTTP URL: http://127.0.0.1:8000"
    )

    print(
        "MCP URL:  http://127.0.0.1:8000/mcp"
    )

    print(
        "=========================================="
    )


    # IMPORTANT:
    # Your installed MCP version does not support
    # port=8001 inside mcp.run().
    #
    # Therefore we use the default port 8000.

    mcp.run(
        transport="streamable-http"
    )


