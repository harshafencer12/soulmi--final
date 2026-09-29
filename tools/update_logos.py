import os

def update_logos():
    print("Running script to update logos...")
    
    html_files = [f for f in os.listdir('.') if f.endswith('.html')]
    
    # Old navbar logo template to match
    old_nav_logo = """                <a href="index.html" class="nav-logo">
                    <svg class="nav-logo-icon" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M20 4L3 17v21h34V17L20 4z" stroke="#9C97C4" stroke-width="2.5" stroke-linejoin="round" fill="rgba(156,151,196,0.08)"/>
                        <path d="M14 40V30a6 6 0 0 1 12 0v10" stroke="#D6B583" stroke-width="2" fill="rgba(214,181,131,0.1)"/>
                        <path d="M20 24s-7-5-7-10c0-3.3 2.7-5 5.5-4 1 .3 1.3 1 1.5 1.5.2-.5.5-1.2 1.5-1.5C24.3 9 27 10.7 27 14c0 5-7 10-7 10z" fill="#D98F76" opacity="0.9"/>
                    </svg>
                    <span class="nav-logo-text">SoulMi.</span>
                </a>"""
                
    new_nav_logo = """                <a href="index.html" class="nav-logo">
                    <img src="images/logo.svg" alt="SoulMi Logo" class="nav-logo-icon">
                    <span class="nav-logo-text">SoulMi</span>
                </a>"""
                
    old_auth_logo = """            <div class="auth-logo">
                <svg class="auth-logo-icon" viewBox="0 0 52 52" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M26 4L4 20v30h44V20L26 4z" stroke="#9C97C4" stroke-width="3" stroke-linejoin="round" fill="rgba(156,151,196,0.08)"/>
                    <path d="M19 52V40a7 7 0 0 1 14 0v12" stroke="#D6B583" stroke-width="2.5" fill="rgba(214,181,131,0.1)"/>
                    <path d="M26 31s-10-7-10-14c0-4.5 3.6-7 8-5.5 1.5.5 2.5 2 3 3 .5-1 1.5-2.5 3-3 4.4-1.5 8 1 8 5.5 0 7-12 14-12 14z" fill="#D98F76" opacity="0.9"/>
                </svg>
            </div>"""
            
    new_auth_logo = """            <div class="auth-logo">
                <img src="images/logo.svg" alt="SoulMi Logo" class="auth-logo-icon" style="width: 52px; height: 52px;">
            </div>"""

    for filename in html_files:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
            
        modified = False
        
        # 1. Update navbar logo
        if old_nav_logo in content:
            content = content.replace(old_nav_logo, new_nav_logo)
            modified = True
            print(f"[REPLACED] Navbar logo in {filename}")
            
        # 2. Update footer brand text
        if '<span class="nav-logo-text">SoulMi.</span>' in content:
            content = content.replace('<span class="nav-logo-text">SoulMi.</span>', '<span class="nav-logo-text">SoulMi</span>')
            modified = True
            print(f"[REPLACED] Footer brand text in {filename}")
            
        # 3. Update auth logo if present (register.html)
        if old_auth_logo in content:
            content = content.replace(old_auth_logo, new_auth_logo)
            modified = True
            print(f"[REPLACED] Auth logo in {filename}")
            
        if modified:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"[SAVED] {filename} updated successfully.")
            
if __name__ == '__main__':
    update_logos()
