import oracledb
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Oracle DBA Assistant")

@mcp.tool()
def active_sessions():
    """
    Get active Oracle sessions
    """

    conn = oracledb.connect(
        user="system",
        password="root",
        dsn="localhost/orclpdb"
    )

    cursor = conn.cursor()

    cursor.execute("""
        SELECT sid,
               serial#,
               username,
               status
        FROM v$session
        WHERE status='ACTIVE'
    """)

    result = cursor.fetchall()

    cursor.close()
    conn.close()

    return result

if __name__ == "__main__":
    mcp.run()