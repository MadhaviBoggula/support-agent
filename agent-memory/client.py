
import asyncio

from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client


# ============================================================
# NEW SERVER PORT
# ============================================================

SERVER_URL = "http://127.0.0.1:8000/mcp"


# ============================================================
# SAVE PROFILE
# ============================================================

async def save_profile(session):

    print("\n========== SAVE NEW PROFILE ==========")

    name = input("Enter name: ")

    while True:

        try:

            age = int(input("Enter age: "))

            if age <= 0 or age >= 120:

                print(
                    "Age must be between 1 and 119."
                )

                continue

            break

        except ValueError:

            print(
                "Please enter a valid number."
            )

    mobile = input("Enter mobile: ")

    location = input("Enter location: ")


    result = await session.call_tool(
        "save_profile",
        {
            "profile": {
                "name": name,
                "age": age,
                "mobile": mobile,
                "location": location
            }
        }
    )


    print("\nServer Response:")

    for content in result.content:

        if hasattr(content, "text"):

            print(content.text)


# ============================================================
# GET ONE PROFILE
# ============================================================

async def get_profile(session):

    print("\n========== GET PROFILE ==========")

    while True:

        try:

            profile_id = int(
                input("Enter profile ID: ")
            )

            if profile_id <= 0:

                print(
                    "ID must be greater than 0."
                )

                continue

            break

        except ValueError:

            print(
                "Please enter a valid ID."
            )


    result = await session.call_tool(
        "get_profile",
        {
            "profile_id": profile_id
        }
    )


    print("\nProfile Details:")

    for content in result.content:

        if hasattr(content, "text"):

            print(content.text)


# ============================================================
# GET ALL PROFILES
# ============================================================

async def get_all_profiles(session):

    print("\n========== ALL PROFILES ==========")

    result = await session.call_tool(
        "get_all_profiles",
        {}
    )


    print("\nAll Saved Profiles:")

    # Print every MCP content item
    for content in result.content:

        if hasattr(content, "text"):

            print(content.text)


# ============================================================
# UPDATE PROFILE
# ============================================================

async def update_profile(session):

    print("\n========== UPDATE PROFILE ==========")

    while True:

        try:

            profile_id = int(
                input("Enter profile ID to update: ")
            )

            if profile_id <= 0:

                print(
                    "ID must be greater than 0."
                )

                continue

            break

        except ValueError:

            print(
                "Please enter a valid ID."
            )


    print(
        """
1. Update Name
2. Update Age
3. Update Mobile
4. Update Location
5. Update Multiple Fields
6. Cancel
"""
    )


    choice = input("Enter your choice: ")


    # --------------------------------------------------------
    # NAME
    # --------------------------------------------------------

    if choice == "1":

        name = input(
            "Enter new name: "
        )

        result = await session.call_tool(
            "update_profile",
            {
                "profile_id": profile_id,
                "profile": {
                    "name": name
                }
            }
        )


        print(
            "\nServer Response:"
        )

        for content in result.content:

            if hasattr(content, "text"):

                print(content.text)


    # --------------------------------------------------------
    # AGE
    # --------------------------------------------------------

    elif choice == "2":

        while True:

            try:

                age = int(
                    input("Enter new age: ")
                )

                if age <= 0 or age >= 120:

                    print(
                        "Age must be between 1 and 119."
                    )

                    continue

                break

            except ValueError:

                print(
                    "Please enter a valid age."
                )


        result = await session.call_tool(
            "update_profile",
            {
                "profile_id": profile_id,
                "profile": {
                    "age": age
                }
            }
        )


        print(
            "\nServer Response:"
        )

        for content in result.content:

            if hasattr(content, "text"):

                print(content.text)


    # --------------------------------------------------------
    # MOBILE
    # --------------------------------------------------------

    elif choice == "3":

        mobile = input(
            "Enter new mobile: "
        )

        result = await session.call_tool(
            "update_profile",
            {
                "profile_id": profile_id,
                "profile": {
                    "mobile": mobile
                }
            }
        )


        print(
            "\nServer Response:"
        )

        for content in result.content:

            if hasattr(content, "text"):

                print(content.text)


    # --------------------------------------------------------
    # LOCATION
    # --------------------------------------------------------

    elif choice == "4":

        location = input(
            "Enter new location: "
        )

        result = await session.call_tool(
            "update_profile",
            {
                "profile_id": profile_id,
                "profile": {
                    "location": location
                }
            }
        )


        print(
            "\nServer Response:"
        )

        for content in result.content:

            if hasattr(content, "text"):

                print(content.text)


    # --------------------------------------------------------
    # MULTIPLE FIELDS
    # --------------------------------------------------------

    elif choice == "5":

        print(
            "\nPress Enter to keep a field unchanged."
        )

        name = input(
            "New name: "
        )

        age_input = input(
            "New age: "
        )

        mobile = input(
            "New mobile: "
        )

        location = input(
            "New location: "
        )


        profile = {}


        if name:

            profile["name"] = name


        if age_input:

            try:

                age = int(age_input)

                if age <= 0 or age >= 120:

                    print(
                        "Invalid age."
                    )

                    return

                profile["age"] = age

            except ValueError:

                print(
                    "Invalid age."
                )

                return


        if mobile:

            profile["mobile"] = mobile


        if location:

            profile["location"] = location


        if not profile:

            print(
                "\nNo changes entered."
            )

            return


        result = await session.call_tool(
            "update_profile",
            {
                "profile_id": profile_id,
                "profile": profile
            }
        )


        print(
            "\nServer Response:"
        )

        for content in result.content:

            if hasattr(content, "text"):

                print(content.text)


    # --------------------------------------------------------
    # CANCEL
    # --------------------------------------------------------

    elif choice == "6":

        print(
            "\nUpdate cancelled."
        )


    else:

        print(
            "\nInvalid choice."
        )


# ============================================================
# MAIN
# ============================================================

async def main():

    print(
        "\n=========================================="
    )

    print(
        "       MCP USER MEMORY SYSTEM"
    )

    print(
        "=========================================="
    )


    # CONNECT TO SERVER ON PORT 8001
    async with streamable_http_client(
        SERVER_URL
    ) as (
        read_stream,
        write_stream,
        _
    ):

        async with ClientSession(
            read_stream,
            write_stream
        ) as session:

            await session.initialize()


            print(
                "\nConnected to MCP Memory Server"
            )

            print(
                f"Server: {SERVER_URL}"
            )


            # GET TOOLS
            tools = await session.list_tools()


            print(
                "\nAvailable MCP Tools:"
            )


            for tool in tools.tools:

                print(
                    f"- {tool.name}"
                )


            # =================================================
            # MENU
            # =================================================

            while True:

                print(
                    "\n=========================================="
                )

                print(
                    "             USER MEMORY MENU"
                )

                print(
                    "=========================================="
                )

                print(
                    "1. Save New Profile"
                )

                print(
                    "2. Get Profile By ID"
                )

                print(
                    "3. Get All Profiles"
                )

                print(
                    "4. Update Profile"
                )

                print(
                    "5. Exit"
                )

                print(
                    "=========================================="
                )


                choice = input(
                    "Enter your choice: "
                )


                if choice == "1":

                    await save_profile(session)


                elif choice == "2":

                    await get_profile(session)


                elif choice == "3":

                    await get_all_profiles(session)


                elif choice == "4":

                    await update_profile(session)


                elif choice == "5":

                    print(
                        "\nExiting MCP User Memory System..."
                    )

                    break


                else:

                    print(
                        "\nInvalid choice. Please try again."
                    )


# ============================================================
# START CLIENT
# ============================================================

if __name__ == "__main__":

    asyncio.run(main())

