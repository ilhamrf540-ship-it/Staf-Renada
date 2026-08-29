import re
with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Fix fetchUsersOnline to merge local users
fetch_users_old = r'''    async function fetchUsersOnline\(\) \{
      const url = getScriptUrl\(\);
      if \(!url\) \{
        try \{
          const localData = JSON\.parse\(localStorage\.getItem\('registeredUsers'\) \|\| '\[\]'\);
          if \(Array\.isArray\(localData\)\) \{
            return localData\.filter\(u => u && typeof u === 'object' && u\.username\);
          \}
        \} catch\(err\) \{\}
        localStorage\.setItem\('registeredUsers', JSON\.stringify\(\[\]\)\);
        return \[\];
      \}
      try \{
        const response = await fetch\(url \+ "\?action=getUsers"\);
        if \(!response\.ok\) \{
          throw new Error\(`HTTP error! status: \$\{response\.status\}`\);
        \}
        const userList = await response\.json\(\);
        if \(Array\.isArray\(userList\)\) \{
          const validUsers = userList\.filter\(u => u && typeof u === 'object' && u\.username\);
          localStorage\.setItem\('registeredUsers', JSON\.stringify\(validUsers\)\);
          return validUsers;
        \}
        throw new Error\("Invalid or empty data from server"\);
      \} catch \(e\) \{
        console\.error\("Error fetching users online:", e\);
        try \{
          const localData = JSON\.parse\(localStorage\.getItem\('registeredUsers'\) \|\| '\[\]'\);
          if \(Array\.isArray\(localData\)\) \{
            return localData\.filter\(u => u && typeof u === 'object' && u\.username\);
          \}
        \} catch\(err\) \{\}
        return \[\];
      \}
    \}'''

fetch_users_new = r'''    async function fetchUsersOnline() {
      const url = getScriptUrl();
      
      // Load local data first
      let localUsers = [];
      try {
        const localData = JSON.parse(localStorage.getItem('registeredUsers') || '[]');
        if (Array.isArray(localData)) {
          localUsers = localData.filter(u => u && typeof u === 'object' && u.username);
        }
      } catch(err) {}

      if (!url) {
        localStorage.setItem('registeredUsers', JSON.stringify(localUsers));
        return localUsers;
      }
      
      try {
        const response = await fetch(url + "?action=getUsers");
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const userList = await response.json();
        if (Array.isArray(userList)) {
          const validUsers = userList.filter(u => u && typeof u === 'object' && u.username);
          
          // MERGE with local to prevent data loss when syncing
          const merged = [...validUsers];
          localUsers.forEach(lu => {
            if (!merged.some(mu => mu.username.toLowerCase() === lu.username.toLowerCase())) {
              merged.push(lu);
            }
          });
          
          localStorage.setItem('registeredUsers', JSON.stringify(merged));
          return merged;
        }
        throw new Error("Invalid or empty data from server");
      } catch (e) {
        console.error("Error fetching users online:", e);
        return localUsers;
      }
    }'''

text = re.sub(fetch_users_old, fetch_users_new, text)

# 2. Fix loadUISettings
load_old = r'''    function loadUISettings\(\) \{
      try \{
        const settings = JSON\.parse\(localStorage\.getItem\('uiSettings'\)\);
        if \(settings\) \{
          // Apply Texts
          const headerTitleEls = document\.querySelectorAll\('header h1, \.login-header h1'\);
          headerTitleEls\.forEach\(el => \{
            if \(settings\.portalTitle\) el\.innerText = settings\.portalTitle;
          \}\);
          
          const headerSubtitleEls = document\.querySelectorAll\('header p, \.login-header p'\);
          headerSubtitleEls\.forEach\(el => \{
            if \(settings\.portalSubtitle\) el\.innerText = settings\.portalSubtitle;
          \}\);

          // Apply Colors
          if \(settings\.bgColorStart && settings\.bgColorEnd\) \{
            document\.body\.style\.background = `linear-gradient\(135deg, \$\{settings\.bgColorStart\} 0%, \$\{settings\.bgColorEnd\} 100%\)`;
          \}
        \}
      \} catch\(e\) \{
        console\.error\("Gagal load UI Settings", e\);
      \}
    \}'''

load_new = r'''    function loadUISettings() {
      try {
        const settings = JSON.parse(localStorage.getItem('uiSettings'));
        if (settings) {
          // Apply Texts
          const headerTitleEls = document.querySelectorAll('header h1, .login-header h1');
          headerTitleEls.forEach(el => {
            if (settings.portalTitle) el.innerText = settings.portalTitle;
          });
          
          const headerSubtitleEls = document.querySelectorAll('header p, .login-header p');
          headerSubtitleEls.forEach(el => {
            if (settings.portalSubtitle) el.innerText = settings.portalSubtitle;
          });

          // Apply Colors
          if (settings.bgColorStart && settings.bgColorEnd) {
            document.body.style.background = `linear-gradient(135deg, ${settings.bgColorStart} 0%, ${settings.bgColorEnd} 100%)`;
          }
          if (settings.primaryColor) {
            document.documentElement.style.setProperty('--primary', settings.primaryColor);
            const style = document.createElement('style');
            style.innerHTML = `
              .btn-primary { background: ${settings.primaryColor} !important; border-color: ${settings.primaryColor} !important; }
              .admin-tab-btn.active { background: ${settings.primaryColor} !important; border-color: ${settings.primaryColor} !important; }
            `;
            document.head.appendChild(style);
          }
          if (settings.fontFamily) {
            document.body.style.fontFamily = settings.fontFamily;
            const h1s = document.querySelectorAll('h1, h2, h3');
            h1s.forEach(h => h.style.fontFamily = settings.fontFamily);
          }
          
          // Apply Logo
          const mainLogo = document.querySelector('.login-header svg, .login-header img');
          if (mainLogo) {
             if (settings.logoUrl) {
                if (mainLogo.tagName.toLowerCase() === 'svg') {
                   const img = document.createElement('img');
                   img.src = settings.logoUrl;
                   img.style.height = '64px';
                   img.style.marginBottom = '1rem';
                   mainLogo.parentNode.replaceChild(img, mainLogo);
                } else {
                   mainLogo.src = settings.logoUrl;
                }
             }
          }

          // Trigger preview update if on settings tab
          if(document.getElementById('previewTitle')) {
             document.getElementById('previewTitle').innerText = settings.portalTitle || 'Portal Evaluasi & Ujian';
             document.getElementById('previewSubtitle').innerText = settings.portalSubtitle || 'Silakan masuk ke dalam sistem';
             document.getElementById('previewLogin').style.background = `linear-gradient(135deg, ${settings.bgColorStart || '#e2e8f0'} 0%, ${settings.bgColorEnd || '#cbd5e1'} 100%)`;
             document.getElementById('previewTitle').style.fontFamily = settings.fontFamily || "'Inter', sans-serif";
             document.getElementById('previewBtn').style.background = settings.primaryColor || '#3b82f6';
             const logoEl = document.getElementById('previewLogo');
             if (settings.logoUrl) {
                 logoEl.src = settings.logoUrl;
             } else {
                 logoEl.src = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='" + encodeURIComponent(settings.primaryColor || '#3b82f6') + "'%3E%3Cpath d='M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5'/%3E%3C/svg%3E";
             }
          }
        }
      } catch(e) {
        console.error("Gagal load UI Settings", e);
      }
    }'''

text = re.sub(load_old, load_new, text)

# 3. Fix saveUISettings and resetUISettings (they are still the old versions)
save_old = r'''    function saveUISettings\(\) \{
      const settings = \{
        portalTitle: document\.getElementById\('uiPortalTitle'\)\.value,
        portalSubtitle: document\.getElementById\('uiPortalSubtitle'\)\.value,
        bgColorStart: document\.getElementById\('uiBgColorStart'\)\.value,
        bgColorEnd: document\.getElementById\('uiBgColorEnd'\)\.value
      \};
      localStorage\.setItem\('uiSettings', JSON\.stringify\(settings\)\);
      loadUISettings\(\);
      showNotification\("Pengaturan Tampilan berhasil disimpan!", "success"\);
    \}

    function resetUISettings\(\) \{
      if\(confirm\("Apakah Anda yakin ingin mengembalikan pengaturan tampilan ke default\?"\)\) \{
        localStorage\.removeItem\('uiSettings'\);
        const headerTitleEls = document\.querySelectorAll\('header h1, \.login-header h1'\);
        headerTitleEls\.forEach\(el => el\.innerText = 'Portal Evaluasi & Ujian'\);
        
        const headerSubtitleEls = document\.querySelectorAll\('header p, \.login-header p'\);
        headerSubtitleEls\.forEach\(el => el\.innerText = 'Silakan masuk ke dalam sistem menggunakan akun Anda'\);
        
        if\(document\.getElementById\('uiPortalTitle'\)\) document\.getElementById\('uiPortalTitle'\)\.value = '';
        if\(document\.getElementById\('uiPortalSubtitle'\)\) document\.getElementById\('uiPortalSubtitle'\)\.value = '';
        if\(document\.getElementById\('uiBgColorStart'\)\) document\.getElementById\('uiBgColorStart'\)\.value = '#e2e8f0';
        if\(document\.getElementById\('uiBgColorEnd'\)\) document\.getElementById\('uiBgColorEnd'\)\.value = '#cbd5e1';
        
        document\.body\.style\.background = '';
        
        showNotification\("Pengaturan dikembalikan ke default\.", "success"\);
      \}
    \}'''

save_new = r'''    function saveUISettings() {
      const settings = {
        portalTitle: document.getElementById('uiPortalTitle').value,
        portalSubtitle: document.getElementById('uiPortalSubtitle').value,
        bgColorStart: document.getElementById('uiBgColorStart').value,
        bgColorEnd: document.getElementById('uiBgColorEnd').value,
        logoUrl: document.getElementById('uiLogoUrl') ? document.getElementById('uiLogoUrl').value : '',
        fontFamily: document.getElementById('uiFontFamily') ? document.getElementById('uiFontFamily').value : "'Inter', sans-serif",
        primaryColor: document.getElementById('uiPrimaryColor') ? document.getElementById('uiPrimaryColor').value : "#3b82f6"
      };
      localStorage.setItem('uiSettings', JSON.stringify(settings));
      loadUISettings();
      showNotification("Pengaturan antarmuka berhasil disimpan.", "success");
    }

    function resetUISettings() {
      if(confirm("Apakah Anda yakin ingin mengembalikan pengaturan tampilan ke default?")) {
        localStorage.removeItem('uiSettings');
        const headerTitleEls = document.querySelectorAll('header h1, .login-header h1');
        headerTitleEls.forEach(el => el.innerText = 'Portal Evaluasi & Ujian');
        
        const headerSubtitleEls = document.querySelectorAll('header p, .login-header p');
        headerSubtitleEls.forEach(el => el.innerText = 'Silakan masuk ke dalam sistem menggunakan akun Anda');
        
        if(document.getElementById('uiPortalTitle')) document.getElementById('uiPortalTitle').value = '';
        if(document.getElementById('uiPortalSubtitle')) document.getElementById('uiPortalSubtitle').value = '';
        if(document.getElementById('uiBgColorStart')) document.getElementById('uiBgColorStart').value = '#e2e8f0';
        if(document.getElementById('uiBgColorEnd')) document.getElementById('uiBgColorEnd').value = '#cbd5e1';
        if(document.getElementById('uiLogoUrl')) document.getElementById('uiLogoUrl').value = '';
        if(document.getElementById('uiFontFamily')) document.getElementById('uiFontFamily').value = "'Inter', sans-serif";
        if(document.getElementById('uiPrimaryColor')) document.getElementById('uiPrimaryColor').value = '#3b82f6';
        
        document.body.style.background = '';
        document.body.style.fontFamily = "'Inter', sans-serif";
        document.documentElement.style.setProperty('--primary', '#3b82f6');
        
        const img = document.querySelector('.login-header img');
        if (img) {
          const svg = document.createElement('div');
          svg.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="var(--primary)" style="width: 64px; height: 64px; margin-bottom: 1rem;"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/></svg>`;
          img.parentNode.replaceChild(svg.firstChild, img);
        }
        
        showNotification("Pengaturan dikembalikan ke default.", "success");
        loadUISettings();
      }
    }'''

text = re.sub(save_old, save_new, text)

# 4. In populateAdminUIForm, update fields
populate_old = r'''        const settings = JSON\.parse\(localStorage\.getItem\('uiSettings'\)\);
        if \(settings\) \{
          if\(document\.getElementById\('uiPortalTitle'\)\) document\.getElementById\('uiPortalTitle'\)\.value = settings\.portalTitle \|\| '';
          if\(document\.getElementById\('uiPortalSubtitle'\)\) document\.getElementById\('uiPortalSubtitle'\)\.value = settings\.portalSubtitle \|\| '';
          if\(document\.getElementById\('uiBgColorStart'\)\) document\.getElementById\('uiBgColorStart'\)\.value = settings\.bgColorStart \|\| '#e2e8f0';
          if\(document\.getElementById\('uiBgColorEnd'\)\) document\.getElementById\('uiBgColorEnd'\)\.value = settings\.bgColorEnd \|\| '#cbd5e1';
        \}'''

populate_new = r'''        const settings = JSON.parse(localStorage.getItem('uiSettings'));
        if (settings) {
          if(document.getElementById('uiPortalTitle')) document.getElementById('uiPortalTitle').value = settings.portalTitle || '';
          if(document.getElementById('uiPortalSubtitle')) document.getElementById('uiPortalSubtitle').value = settings.portalSubtitle || '';
          if(document.getElementById('uiBgColorStart')) document.getElementById('uiBgColorStart').value = settings.bgColorStart || '#e2e8f0';
          if(document.getElementById('uiBgColorEnd')) document.getElementById('uiBgColorEnd').value = settings.bgColorEnd || '#cbd5e1';
          if(document.getElementById('uiLogoUrl')) document.getElementById('uiLogoUrl').value = settings.logoUrl || '';
          if(document.getElementById('uiFontFamily')) document.getElementById('uiFontFamily').value = settings.fontFamily || "'Inter', sans-serif";
          if(document.getElementById('uiPrimaryColor')) document.getElementById('uiPrimaryColor').value = settings.primaryColor || '#3b82f6';
        }'''

text = re.sub(populate_old, populate_new, text)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)
print("Done!")
