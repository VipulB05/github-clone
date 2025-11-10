import streamlit as st
from database import get_database
from datetime import datetime


def create_repository(name, description, visibility, owner_id):
    """Create a new repository"""
    db = get_database()
    
    # Check if repo name already exists for this user
    check_query = """
        SELECT * FROM REPO 
        WHERE Name = %s AND OwnerID = %s
    """
    existing = db.execute_query(check_query, (name, owner_id), fetch=True)
    
    if existing:
        return False, "Repository name already exists"
    
    query = """
        INSERT INTO REPO (Name, Description, Visibility, OwnerID)
        VALUES (%s, %s, %s, %s)
    """
    repo_id = db.execute_query(query, (name, description, visibility, owner_id))
    
    if repo_id:
        # Create default main branch
        branch_query = """
            INSERT INTO BRANCH (Name, CreatedBy, RID, Status)
            VALUES ('main', %s, %s, 'Active')
        """
        db.execute_query(branch_query, (owner_id, repo_id))
        return True, repo_id
    
    return False, "Failed to create repository"


def get_user_repositories(user_id):
    """Get all repositories owned by user"""
    db = get_database()
    query = """
        SELECT r.*, 
               (SELECT COUNT(*) FROM BRANCH WHERE RID = r.RID) as branch_count,
               (SELECT COUNT(*) FROM REQUEST WHERE RID = r.RID) as request_count
        FROM REPO r
        WHERE r.OwnerID = %s
        ORDER BY r.CreatedOn DESC
    """
    return db.execute_query(query, (user_id,), fetch=True)


def get_public_repositories():
    """Get all public repositories"""
    db = get_database()
    query = """
        SELECT r.*, u.Fname, u.Lname,
               (SELECT COUNT(*) FROM BRANCH WHERE RID = r.RID) as branch_count
        FROM REPO r
        INNER JOIN USER u ON r.OwnerID = u.UID
        WHERE r.Visibility = 'Public'
        ORDER BY r.CreatedOn DESC
    """
    return db.execute_query(query, fetch=True)


def get_repository(repo_id):
    """Get repository details"""
    db = get_database()
    query = """
        SELECT r.*, u.Fname, u.Lname
        FROM REPO r
        INNER JOIN USER u ON r.OwnerID = u.UID
        WHERE r.RID = %s
    """
    result = db.execute_query(query, (repo_id,), fetch=True)
    return result[0] if result else None


def update_repository(repo_id, name, description, visibility):
    """Update repository details"""
    db = get_database()
    query = """
        UPDATE REPO 
        SET Name = %s, Description = %s, Visibility = %s
        WHERE RID = %s
    """
    result = db.execute_query(query, (name, description, visibility, repo_id))
    return result is not False


def delete_repository(repo_id):
    """Delete a repository"""
    db = get_database()
    query = "DELETE FROM REPO WHERE RID = %s"
    result = db.execute_query(query, (repo_id,))
    return result is not False


def get_repository_branches(repo_id):
    """Get all branches for a repository"""
    db = get_database()
    query = """
        SELECT b.*, u.Fname, u.Lname
        FROM BRANCH b
        INNER JOIN USER u ON b.CreatedBy = u.UID
        WHERE b.RID = %s
        ORDER BY b.CreatedOn DESC
    """
    return db.execute_query(query, (repo_id,), fetch=True)


def create_branch(name, repo_id, created_by):
    """Create a new branch"""
    db = get_database()
    
    # Check if branch name exists
    check_query = """
        SELECT * FROM BRANCH 
        WHERE Name = %s AND RID = %s
    """
    existing = db.execute_query(check_query, (name, repo_id), fetch=True)
    
    if existing:
        return False, "Branch name already exists"
    
    query = """
        INSERT INTO BRANCH (Name, CreatedBy, RID, Status)
        VALUES (%s, %s, %s, 'Active')
    """
    branch_id = db.execute_query(query, (name, created_by, repo_id))
    return (True, branch_id) if branch_id else (False, "Failed to create branch")


def get_branch_commits(branch_id):
    """Get all commits for a branch"""
    db = get_database()
    query = """
        SELECT c.*, u.Fname, u.Lname
        FROM COMMIT c
        INNER JOIN USER u ON c.UID = u.UID
        WHERE c.BID = %s
        ORDER BY c.CommitDate DESC, c.CommitTime DESC
    """
    return db.execute_query(query, (branch_id,), fetch=True)


def create_commit(message, branch_id, user_id):
    """Create a new commit"""
    db = get_database()
    
    now = datetime.now()
    query = """
        INSERT INTO COMMIT (Message, CommitTime, CommitDate, BID, UID)
        VALUES (%s, %s, %s, %s, %s)
    """
    commit_id = db.execute_query(query, 
                                  (message, now.time(), now.date(), branch_id, user_id))
    
    if commit_id:
        # Update branch commit count
        update_query = """
            UPDATE BRANCH 
            SET CommitCount = CommitCount + 1
            WHERE BID = %s
        """
        db.execute_query(update_query, (branch_id,))
        return True, commit_id
    
    return False, "Failed to create commit"


def _get_or_create_anon_user():
    """Ensure an anonymous user exists and return its UID.

    This uses a simple placeholder user record so commits can be attributed
    to a stable anonymized account. Password is kept empty string to satisfy
    NOT NULL constraint in schema.
    """
    db = get_database()
    # Try to find an existing anonymous user
    query = "SELECT UID FROM USER WHERE Fname = %s AND Password = %s"
    res = db.execute_query(query, ('Anonymous', ''), fetch=True)
    if res:
        return res[0]['UID']

    # Create anonymous user
    insert = "INSERT INTO USER (Fname, Lname, Password) VALUES (%s, %s, %s)"
    uid = db.execute_query(insert, ('Anonymous', 'User', ''))
    return uid


def create_public_commit(message, branch_id, author_name=None, author_email=None):
    """Create a commit on a branch for public repositories without requiring auth.

    - Validates that the branch belongs to a repository with Visibility = 'Public'.
    - Attributes the commit to a shared anonymous user and prefixes the commit
      message with any provided author name/email for basic auditability.
    """
    db = get_database()

    # Verify branch and repository visibility
    q = "SELECT r.Visibility FROM BRANCH b JOIN REPO r ON b.RID = r.RID WHERE b.BID = %s"
    res = db.execute_query(q, (branch_id,), fetch=True)
    if not res:
        return False, "Branch not found"

    visibility = res[0].get('Visibility')
    if visibility != 'Public':
        return False, "Repository is not public"

    # Build an annotated commit message including author metadata when provided
    prefix_parts = []
    if author_name:
        prefix_parts.append(str(author_name))
    if author_email:
        prefix_parts.append(f"<{author_email}>")

    prefix = ''
    if prefix_parts:
        prefix = '[Public Commit: ' + ' '.join(prefix_parts) + '] '

    full_message = prefix + (message or '')

    # Use or create anonymous user as the committer
    anon_uid = _get_or_create_anon_user()
    if not anon_uid:
        return False, "Failed to create anonymous user"

    # Reuse existing create_commit implementation for bookkeeping
    return create_commit(full_message, branch_id, anon_uid)


def create_request(request_type, repo_id, created_by):
    """Create a pull/merge request"""
    db = get_database()
    
    query = """
        INSERT INTO REQUEST (RequestType, CreatedBy, RID, Status)
        VALUES (%s, %s, %s, 'Open')
    """
    request_id = db.execute_query(query, (request_type, created_by, repo_id))
    return (True, request_id) if request_id else (False, "Failed to create request")


def get_repository_requests(repo_id):
    """Get all requests for a repository"""
    db = get_database()
    query = """
        SELECT r.*, u.Fname, u.Lname
        FROM REQUEST r
        INNER JOIN USER u ON r.CreatedBy = u.UID
        WHERE r.RID = %s
        ORDER BY r.CreatedOn DESC
    """
    return db.execute_query(query, (repo_id,), fetch=True)
