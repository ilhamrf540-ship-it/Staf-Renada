import re

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx1 = text.find('function saveUISettings() {')
if idx1 != -1:
    idx2 = text.find('function resetUISettings() {', idx1)
    idx3 = text.find('}', text.find('}', text.find('}', text.find('}', idx2) + 1) + 1) + 1) + 1
    
    old_code = text[idx1:idx3+1]

    new_code = r'''function saveUISettings() {
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
    
    text = text[:idx1] + new_code + text[idx3+2:]
    
    # 4. In populateAdminUIForm, update fields
    populate_old = r'''        const settings = JSON.parse(localStorage.getItem('uiSettings'));
        if (settings) {
          if(document.getElementById('uiPortalTitle')) document.getElementById('uiPortalTitle').value = settings.portalTitle || '';
          if(document.getElementById('uiPortalSubtitle')) document.getElementById('uiPortalSubtitle').value = settings.portalSubtitle || '';
          if(document.getElementById('uiBgColorStart')) document.getElementById('uiBgColorStart').value = settings.bgColorStart || '#e2e8f0';
          if(document.getElementById('uiBgColorEnd')) document.getElementById('uiBgColorEnd').value = settings.bgColorEnd || '#cbd5e1';
        }'''

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

    text = text.replace(populate_old, populate_new)

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Replaced successfully!")
else:
    print("Could not find function saveUISettings()")
