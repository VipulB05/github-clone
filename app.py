import streamlit as st
from config import APP_CONFIG, UI_COLORS
from auth import signup_user, login_user, get_user_email
from repositories import (
    create_repository, get_user_repositories, get_public_repositories,
    get_repository, update_repository, delete_repository,
    get_repository_branches, create_branch, get_branch_commits,
    create_commit, create_request, get_repository_requests,
    create_public_commit
)

# Page configuration
st.set_page_config(
    page_title=APP_CONFIG['page_title'],
    page_icon=APP_CONFIG['page_icon'],
    layout=APP_CONFIG['layout'],
    initial_sidebar_state="expanded"
)

# Custom CSS for modern dark UI
st.markdown("""
<style>
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Main content area */
    .main {
        padding: 2rem;
        background-color: #0D1117;
    }
    
    /* Custom card styling - Dark Mode */
    .custom-card {
        background: #161B22;
        border: 1px solid #30363D;
        border-radius: 8px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.3);
        transition: all 0.2s ease;
    }
    
    .custom-card:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.5);
        border-color: #58A6FF;
    }
    
    /* Header styles - Dark Mode */
    .page-header {
        font-size: 2rem;
        font-weight: 700;
        color: #C9D1D9;
        margin-bottom: 0.5rem;
        padding-bottom: 1rem;
        border-bottom: 2px solid #30363D;
    }
    
    .section-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #C9D1D9;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }
    
    /* Badge styles - Dark Mode */
    .badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 500;
        margin-right: 8px;
    }
    
    .badge-public {
        background: rgba(88, 166, 255, 0.15);
        color: #58A6FF;
        border: 1px solid #388BFD;
    }
    
    .badge-private {
        background: rgba(210, 153, 34, 0.15);
        color: #D29922;
        border: 1px solid #BB8009;
    }
    
    .badge-active {
        background: rgba(63, 185, 80, 0.15);
        color: #3FB950;
        border: 1px solid #2EA043;
    }
    
    .badge-open {
        background: rgba(63, 185, 80, 0.15);
        color: #3FB950;
        border: 1px solid #2EA043;
    }
    
    .badge-closed {
        background: rgba(248, 81, 73, 0.15);
        color: #F85149;
        border: 1px solid #DA3633;
    }
    
    /* Button styling - Dark Mode */
    .stButton > button {
        border-radius: 6px;
        font-weight: 500;
        border: 1px solid #30363D;
        transition: all 0.2s ease;
        background-color: #21262D;
        color: #C9D1D9;
    }
    
    .stButton > button:hover {
        background: #30363D;
        border-color: #58A6FF;
    }
    
    /* Form styling - Dark Mode */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select {
        border-radius: 6px;
        border: 1px solid #30363D;
        background-color: #0D1117;
        color: #C9D1D9;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus,
    .stSelectbox > div > div > select:focus {
        border-color: #58A6FF;
    }
    
    /* Sidebar styling - Dark Mode */
    [data-testid="stSidebar"] {
        background: #161B22;
        border-right: 1px solid #30363D;
    }
    
    /* Metric styling - Dark Mode */
    .stat-box {
        background: #0D1117;
        padding: 12px;
        border-radius: 6px;
        text-align: center;
        border: 1px solid #30363D;
    }
    
    .stat-number {
        font-size: 1.5rem;
        font-weight: 700;
        color: #58A6FF;
    }
    
    .stat-label {
        font-size: 0.875rem;
        color: #8B949E;
        margin-top: 4px;
    }
    
    /* Repo card specific - Dark Mode */
    .repo-title {
        font-size: 1.25rem;
        font-weight: 600;
        color: #58A6FF;
        margin-bottom: 8px;
    }
    
    .repo-description {
        color: #8B949E;
        font-size: 0.95rem;
        margin-bottom: 12px;
    }
    
    .repo-meta {
        display: flex;
        gap: 16px;
        font-size: 0.875rem;
        color: #8B949E;
    }
    
    /* Divider - Dark Mode */
    .custom-divider {
        height: 1px;
        background: #30363D;
        margin: 1.5rem 0;
    }
    
    /* Tab styling - Dark Mode */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #0D1117;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 6px 6px 0 0;
        padding: 12px 20px;
        font-weight: 500;
        background-color: #161B22;
        color: #8B949E;
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background-color: #0D1117;
        color: #C9D1D9;
        border-bottom: 2px solid #58A6FF;
    }
    
    /* User profile in sidebar - Dark Mode */
    .user-profile {
        background: #0D1117;
        padding: 16px;
        border-radius: 8px;
        border: 1px solid #30363D;
        margin-bottom: 16px;
    }
    
    .user-name {
        font-weight: 600;
        color: #C9D1D9;
        font-size: 1rem;
    }
    
    .user-email {
        color: #8B949E;
        font-size: 0.875rem;
        margin-top: 4px;
    }
    
    /* Additional dark mode fixes */
    .stMarkdown {
        color: #C9D1D9;
    }
    
    .stAlert {
        background-color: #161B22;
        border: 1px solid #30363D;
        color: #C9D1D9;
    }
    
    /* Caption text */
    .stCaptionContainer {
        color: #8B949E;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user' not in st.session_state:
    st.session_state.user = None
if 'page' not in st.session_state:
    st.session_state.page = 'home'


def logout():
    """Logout user"""
    st.session_state.logged_in = False
    st.session_state.user = None
    st.session_state.page = 'home'
    st.rerun()


def show_login_signup():
    """Show login and signup forms"""
    # Center the login form
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<div class="page-header" style="text-align: center; border: none;">GitHub Clone</div>', unsafe_allow_html=True)
        st.markdown('<p style="text-align: center; color: #8B949E; margin-bottom: 2rem;">Collaborate, share, and build amazing projects</p>', unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["Sign In", "Sign Up"])
        
        with tab1:
            st.markdown('<div style="padding: 20px 0;">', unsafe_allow_html=True)
            with st.form("login_form"):
                email = st.text_input("Email Address", placeholder="you@example.com")
                password = st.text_input("Password", type="password", placeholder="Enter your password")
                
                col_a, col_b = st.columns([2, 1])
                with col_a:
                    submit = st.form_submit_button("Sign In", use_container_width=True, type="primary")
                
                if submit:
                    if email and password:
                        success, user_data = login_user(email, password)
                        if success:
                            st.session_state.logged_in = True
                            st.session_state.user = user_data
                            st.success("Welcome back!")
                            st.rerun()
                        else:
                            st.error("Invalid email or password")
                    else:
                        st.error("Please fill in all fields")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with tab2:
            st.markdown('<div style="padding: 20px 0;">', unsafe_allow_html=True)
            with st.form("signup_form"):
                col_fn, col_ln = st.columns(2)
                with col_fn:
                    fname = st.text_input("First Name", placeholder="John")
                with col_ln:
                    lname = st.text_input("Last Name", placeholder="Doe")
                
                email = st.text_input("Email Address", placeholder="you@example.com")
                phoneno = st.text_input("Phone Number (Optional)", placeholder="+1 234 567 8900")
                
                col_p1, col_p2 = st.columns(2)
                with col_p1:
                    password = st.text_input("Password", type="password", placeholder="Min. 8 characters")
                with col_p2:
                    confirm_password = st.text_input("Confirm Password", type="password", placeholder="Re-enter password")
                
                submit = st.form_submit_button("Create Account", use_container_width=True, type="primary")
                
                if submit:
                    if fname and email and password:
                        if password == confirm_password:
                            success, message = signup_user(fname, lname, email, password, phoneno)
                            if success:
                                st.success("Account created successfully! Please sign in.")
                            else:
                                st.error(message)
                        else:
                            st.error("Passwords do not match")
                    else:
                        st.error("Please fill in all required fields")
            st.markdown('</div>', unsafe_allow_html=True)


def show_home():
    """Show home page with public repositories"""
    st.markdown('<div class="page-header">Discover Repositories</div>', unsafe_allow_html=True)
    
    repos = get_public_repositories()
    
    if repos:
        for repo in repos:
            st.markdown(f"""
            <div class="custom-card">
                <div class="repo-title">{repo['Name']}</div>
                <div style="color: #8B949E; font-size: 0.9rem; margin-bottom: 8px;">
                    by {repo['Fname']} {repo['Lname']}
                </div>
                <div class="repo-description">{repo['Description'] or 'No description provided'}</div>
                <div class="repo-meta">
                    <span>◉ {repo['branch_count']} branches</span>
                    <span>• Created {repo['CreatedOn'].strftime('%b %d, %Y')}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            # Add a button to view any public repo
            if st.button("View Repository", key=f"view_public_{repo['RID']}", use_container_width=False):
                st.session_state.selected_repo = repo['RID']
                st.session_state.page = 'view_repo'
                st.rerun()
            st.markdown('<div style="height: 1rem;"></div>', unsafe_allow_html=True)
    else:
        st.info("No public repositories available yet. Create your first repository!")


def show_my_repositories():
    """Show user's repositories"""
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown('<div class="page-header">My Repositories</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div style="padding-top: 1rem;">', unsafe_allow_html=True)
        if st.button("New Repository", use_container_width=True, type="primary"):
            st.session_state.page = 'create_repo'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    repos = get_user_repositories(st.session_state.user['UID'])
    
    if repos:
        for repo in repos:
            visibility_badge = 'badge-public' if repo['Visibility'] == 'Public' else 'badge-private'
            st.markdown(f"""
            <div class="custom-card">
                <div style="display: flex; justify-content: space-between; align-items: start;">
                    <div style="flex: 1;">
                        <div class="repo-title">{repo['Name']}</div>
                        <div class="repo-description">{repo['Description'] or 'No description provided'}</div>
                        <div style="margin-top: 12px;">
                            <span class="badge {visibility_badge}">{repo['Visibility']}</span>
                        </div>
                    </div>
                    <div style="text-align: right;">
                        <div class="stat-box" style="min-width: 120px;">
                            <div class="stat-number">{repo['branch_count']}</div>
                            <div class="stat-label">Branches</div>
                        </div>
                        <div class="stat-box" style="min-width: 120px; margin-top: 8px;">
                            <div class="stat-number">{repo['request_count']}</div>
                            <div class="stat-label">Requests</div>
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("View Repository", key=f"view_{repo['RID']}", use_container_width=False):
                st.session_state.selected_repo = repo['RID']
                st.session_state.page = 'view_repo'
                st.rerun()
            st.markdown('<div style="height: 1rem;"></div>', unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="custom-card" style="text-align: center; padding: 40px;">
            <div style="font-size: 1.2rem; color: #8B949E; margin-bottom: 16px;">
                You haven't created any repositories yet
            </div>
            <div style="color: #8B949E;">
                Get started by creating your first repository
            </div>
        </div>
        """, unsafe_allow_html=True)


def show_create_repository():
    """Show create repository form"""
    st.markdown('<div class="page-header">Create New Repository</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="custom-card">
    """, unsafe_allow_html=True)
    
    with st.form("create_repo_form"):
        st.markdown('<div class="section-header" style="margin-top: 0;">Repository Details</div>', unsafe_allow_html=True)
        
        name = st.text_input("Repository Name *", placeholder="my-awesome-project")
        st.caption("Great repository names are short and memorable")
        
        description = st.text_area("Description", placeholder="A brief description of your repository", height=100)
        st.caption("Help others understand what your repository is about")
        
        visibility = st.selectbox("Visibility", ["Public", "Private"], 
                                  help="Public repositories are visible to everyone. Private repositories are only visible to you.")
        
        st.markdown('<div style="margin-top: 2rem;"></div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 4])
        with col1:
            submit = st.form_submit_button("Create Repository", use_container_width=True, type="primary")
        with col2:
            cancel = st.form_submit_button("Cancel", use_container_width=True)
        
        if submit:
            if name:
                success, result = create_repository(
                    name, description, visibility, st.session_state.user['UID']
                )
                if success:
                    st.success("Repository created successfully!")
                    st.session_state.page = 'my_repos'
                    st.rerun()
                else:
                    st.error(result)
            else:
                st.error("Repository name is required")
        
        if cancel:
            st.session_state.page = 'my_repos'
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)


def show_repository_details():
    """Show repository details with branches and commits"""
    repo_id = st.session_state.selected_repo
    repo = get_repository(repo_id)
    
    if not repo:
        st.error("Repository not found")
        return
    
    # Repository header
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f'<div class="page-header">{repo["Name"]}</div>', unsafe_allow_html=True)
    with col2:
        if st.button("← Back", use_container_width=True):
            st.session_state.page = 'my_repos'
            st.rerun()
    
    # Repository info card
    visibility_badge = 'badge-public' if repo['Visibility'] == 'Public' else 'badge-private'
    st.markdown(f"""
    <div class="custom-card">
        <div style="color: #8B949E; margin-bottom: 8px;">
            by {repo['Fname']} {repo['Lname']}
        </div>
        <div class="repo-description">{repo['Description'] or 'No description provided'}</div>
        <span class="badge {visibility_badge}">{repo['Visibility']}</span>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["Branches", "Commits", "Pull Requests", "Settings"])
    
    with tab1:
        st.markdown('<div class="section-header">Branches</div>', unsafe_allow_html=True)
        
        # Add new branch
        if repo['OwnerID'] == st.session_state.user['UID']:
            with st.expander("Create New Branch", expanded=False):
                with st.form("create_branch_form"):
                    branch_name = st.text_input("Branch Name", placeholder="feature/new-feature")
                    st.caption("Choose a descriptive name for your branch")
                    submit = st.form_submit_button("Create Branch", use_container_width=True, type="primary")
                    
                    if submit and branch_name:
                        success, result = create_branch(
                            branch_name, repo_id, st.session_state.user['UID']
                        )
                        if success:
                            st.success("Branch created successfully!")
                            st.rerun()
                        else:
                            st.error(result)
        
        # List branches
        branches = get_repository_branches(repo_id)
        if branches:
            for branch in branches:
                status_badge = 'badge-active' if branch['Status'] == 'Active' else 'badge-closed'
                st.markdown(f"""
                <div class="custom-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <div style="font-size: 1.1rem; font-weight: 600; color: #C9D1D9; margin-bottom: 8px;">
                                {branch['Name']}
                            </div>
                            <div style="color: #8B949E; font-size: 0.9rem;">
                                Created by {branch['Fname']} {branch['Lname']} • {branch['CreatedOn'].strftime('%b %d, %Y')}
                            </div>
                            <div style="margin-top: 8px;">
                                <span class="badge {status_badge}">{branch['Status']}</span>
                                <span style="color: #8B949E; margin-left: 12px;">● {branch['CommitCount']} commits</span>
                            </div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No branches in this repository yet")
    
    with tab2:
        st.markdown('<div class="section-header">Commits</div>', unsafe_allow_html=True)
        
        # Select branch
        branches = get_repository_branches(repo_id)
        if branches:
            branch_names = {b['BID']: b['Name'] for b in branches}
            selected_branch_id = st.selectbox(
                "Branch",
                options=list(branch_names.keys()),
                format_func=lambda x: branch_names[x],
                label_visibility="collapsed"
            )

            # DEBUG: Show key context for diagnosing public commit logic
            st.markdown(f"""
            <div style='background:#21262D;padding:8px;border-radius:6px;margin-bottom:8px;'>
            <b>DEBUG INFO</b><br>
            <b>Repo Visibility:</b> {repo.get('Visibility')}<br>
            <b>Repo Owner UID:</b> {repo.get('OwnerID')}<br>
            <b>Current User UID:</b> {st.session_state.user['UID'] if 'user' in st.session_state else 'None'}<br>
            <b>Selected Branch ID:</b> {selected_branch_id}
            </div>
            """, unsafe_allow_html=True)
            
            # Create commit
            if repo['OwnerID'] == st.session_state.user['UID']:
                with st.expander("New Commit", expanded=False):
                    with st.form("create_commit_form"):
                        message = st.text_area("Commit Message", placeholder="Describe your changes...", height=100)
                        st.caption("Write a clear and concise commit message")
                        submit = st.form_submit_button("Commit Changes", use_container_width=True, type="primary")
                        
                        if submit and message:
                            success, result = create_commit(
                                message, selected_branch_id, st.session_state.user['UID']
                            )
                            if success:
                                st.success("Commit created successfully!")
                                st.rerun()
                            else:
                                st.error(result)

            # Allow public (anonymous) commits to public repositories
            # If the repository is public, show a lightweight form for unauthenticated
            # or non-owner visitors to submit a commit. These commits are attributed
            # to an anonymous account and include optional author metadata.
            try:
                current_user_uid = st.session_state.user['UID']
            except Exception:
                current_user_uid = None

            # Show public commit form for any logged-in user who is NOT the repo owner
            if repo.get('Visibility') == 'Public' and current_user_uid and current_user_uid != repo['OwnerID']:
                with st.expander("Public Commit (anyone)", expanded=False):
                    with st.form("public_commit_form"):
                        author_name = st.text_input("Name (optional)")
                        author_email = st.text_input("Email (optional)")
                        pub_message = st.text_area("Commit Message", placeholder="Describe your changes...", height=100)
                        submit_pub = st.form_submit_button("Submit Public Commit", use_container_width=True, type="secondary")

                        if submit_pub:
                            if not pub_message:
                                st.error("Please enter a commit message")
                            else:
                                success, result = create_public_commit(pub_message, selected_branch_id, author_name or None, author_email or None)
                                if success:
                                    st.success("Public commit created successfully!")
                                    st.rerun()
                                else:
                                    st.error(result)
            
            st.markdown('<div style="margin-top: 1.5rem;"></div>', unsafe_allow_html=True)
            
            # List commits
            commits = get_branch_commits(selected_branch_id)
            if commits:
                for commit in commits:
                    st.markdown(f"""
                    <div class="custom-card">
                        <div style="font-weight: 600; color: #C9D1D9; margin-bottom: 8px;">
                            {commit['Message']}
                        </div>
                        <div style="color: #8B949E; font-size: 0.9rem;">
                            {commit['Fname']} {commit['Lname']} committed on {commit['CommitDate'].strftime('%b %d, %Y')} at {str(commit['CommitTime'])[:8]}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No commits on this branch yet")
    
    with tab3:
        st.markdown('<div class="section-header">Pull Requests</div>', unsafe_allow_html=True)
        
        # Create request
        if repo['OwnerID'] == st.session_state.user['UID']:
            with st.expander("New Pull Request", expanded=False):
                with st.form("create_request_form"):
                    request_type = st.selectbox("Request Type", ["Pull", "Merge"])
                    st.caption("Pull requests let you tell others about changes you've pushed")
                    submit = st.form_submit_button("Create Request", use_container_width=True, type="primary")
                    
                    if submit:
                        success, result = create_request(
                            request_type, repo_id, st.session_state.user['UID']
                        )
                        if success:
                            st.success("Request created successfully!")
                            st.rerun()
                        else:
                            st.error(result)
        
        st.markdown('<div style="margin-top: 1.5rem;"></div>', unsafe_allow_html=True)
        
        # List requests
        requests = get_repository_requests(repo_id)
        if requests:
            for req in requests:
                status_badge_class = 'badge-open' if req['Status'] == 'Open' else 'badge-closed'
                st.markdown(f"""
                <div class="custom-card">
                    <div style="display: flex; justify-content: space-between; align-items: start;">
                        <div style="flex: 1;">
                            <div style="font-size: 1.1rem; font-weight: 600; color: #C9D1D9; margin-bottom: 8px;">
                                {req['RequestType']} Request #{req['ReqID']}
                            </div>
                            <div style="color: #8B949E; font-size: 0.9rem; margin-bottom: 8px;">
                                Opened by {req['Fname']} {req['Lname']} on {req['CreatedOn'].strftime('%b %d, %Y')}
                            </div>
                            <span class="badge {status_badge_class}">{req['Status']}</span>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No pull requests yet")
    
    with tab4:
        if repo['OwnerID'] == st.session_state.user['UID']:
            st.markdown('<div class="section-header">Repository Settings</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="custom-card">', unsafe_allow_html=True)
            with st.form("update_repo_form"):
                st.markdown("**General Settings**")
                name = st.text_input("Repository Name", value=repo['Name'])
                description = st.text_area("Description", value=repo['Description'] or '', height=100)
                visibility = st.selectbox(
                    "Visibility",
                    ["Public", "Private"],
                    index=0 if repo['Visibility'] == 'Public' else 1
                )
                
                st.markdown('<div style="margin-top: 2rem;"></div>', unsafe_allow_html=True)
                
                col1, col2 = st.columns([1, 4])
                with col1:
                    update = st.form_submit_button("Save Changes", use_container_width=True, type="primary")
                
                if update:
                    if update_repository(repo_id, name, description, visibility):
                        st.success("Repository updated successfully!")
                        st.rerun()
                    else:
                        st.error("Failed to update repository")
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Danger zone
            st.markdown('<div style="margin-top: 2rem;"></div>', unsafe_allow_html=True)
            st.markdown('<div class="custom-card" style="border-color: #F85149;">', unsafe_allow_html=True)
            st.markdown('<div style="color: #F85149; font-weight: 600; font-size: 1.1rem; margin-bottom: 8px;">Danger Zone</div>', unsafe_allow_html=True)
            st.markdown('<div style="color: #8B949E; margin-bottom: 16px;">Once you delete a repository, there is no going back. Please be certain.</div>', unsafe_allow_html=True)
            
            if st.button("Delete Repository", type="secondary", use_container_width=False):
                if delete_repository(repo_id):
                    st.success("Repository deleted successfully!")
                    st.session_state.page = 'my_repos'
                    st.rerun()
                else:
                    st.error("Failed to delete repository")
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("Only the repository owner can access settings")


def main():
    """Main application"""
    
    # Sidebar navigation
    if st.session_state.logged_in:
        with st.sidebar:
            # App branding
            st.markdown("""
            <div style="text-align: center; padding: 1rem 0; margin-bottom: 1.5rem;">
                <h2 style="color: #58A6FF; margin: 0; font-weight: 700;">GitHub Clone</h2>
                <p style="color: #8B949E; font-size: 0.85rem; margin-top: 4px;">Version Control System</p>
            </div>
            """, unsafe_allow_html=True)
            
            # User profile card
            user_email = get_user_email(st.session_state.user['UID'])
            st.markdown(f"""
            <div class="user-profile">
                <div class="user-name">{st.session_state.user['Fname']} {st.session_state.user['Lname']}</div>
                <div class="user-email">{user_email}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Navigation buttons
            st.markdown('<div style="margin-top: 1.5rem;"></div>', unsafe_allow_html=True)
            
            nav_button_style = "primary" if st.session_state.page == 'home' else "secondary"
            if st.button("Home", use_container_width=True, type=nav_button_style):
                st.session_state.page = 'home'
                st.rerun()
            
            nav_button_style = "primary" if st.session_state.page in ['my_repos', 'create_repo', 'view_repo'] else "secondary"
            if st.button("My Repositories", use_container_width=True, type=nav_button_style):
                st.session_state.page = 'my_repos'
                st.rerun()
            
            # Logout at bottom
            st.markdown('<div style="position: fixed; bottom: 20px; width: 240px;">', unsafe_allow_html=True)
            if st.button("Sign Out", use_container_width=True):
                logout()
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Route to appropriate page
    if not st.session_state.logged_in:
        show_login_signup()
    else:
        page = st.session_state.page
        
        if page == 'home':
            show_home()
        elif page == 'my_repos':
            show_my_repositories()
        elif page == 'create_repo':
            show_create_repository()
        elif page == 'view_repo':
            show_repository_details()


if __name__ == "__main__":
    main()
