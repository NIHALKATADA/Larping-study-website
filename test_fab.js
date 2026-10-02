const puppeteer = require('puppeteer');

(async () => {
    const browser = await puppeteer.launch({ headless: true });
    const page = await browser.newPage();
    page.on('console', msg => console.log('PAGE LOG:', msg.text()));
    page.on('pageerror', error => console.log('PAGE ERROR:', error.message));
    
    await page.goto('file:///' + __dirname + '/subjects/ml/midterm-important.html');
    
    // Check if fabMainBtn exists
    const fabBtn = await page.$('#fabMainBtn');
    console.log('Found fabBtn:', !!fabBtn);
    
    // Click fabBtn
    await fabBtn.click();
    console.log('Clicked fabBtn');
    
    // Check if menu is open
    const isOpen = await page.$eval('#fabMenu', el => el.classList.contains('open'));
    console.log('fabMenu is open after click:', isOpen);
    
    // Click a button inside menu
    const filterBtn = await page.$('button[title="Filters"]');
    if (filterBtn) {
        await filterBtn.click();
        console.log('Clicked Filter button');
    }
    
    // Check if filter modal is active
    const isModalActive = await page.$eval('#filterModal', el => el.classList.contains('active'));
    console.log('Filter modal active:', isModalActive);
    
    // Try click outside
    await page.mouse.click(10, 10);
    const isMenuStillOpen = await page.$eval('#fabMenu', el => el.classList.contains('open'));
    console.log('fabMenu is open after clicking outside:', isMenuStillOpen);
    
    await browser.close();
})();
