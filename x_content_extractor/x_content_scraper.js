const { chromium } = require('playwright');

async function scrapeXContent(url) {
  // 启动浏览器，模拟真实用户环境
  const browser = await chromium.launch({
    headless: true, // 无头模式，更适合服务器环境
    args: [
      '--no-sandbox',
      '--disable-setuid-sandbox',
      '--disable-dev-shm-usage',
      '--disable-accelerated-2d-canvas',
      '--no-first-run',
      '--no-zygote',
      '--disable-gpu',
      '--disable-web-security',
      '--allow-running-insecure-content',
      '--disable-features=VizDisplayCompositor',
      '--disable-extensions',
      '--disable-ipc-flooding-protection',
      '--disable-background-timer-throttling',
      '--disable-backgrounding-occluded-windows',
      '--disable-renderer-backgrounding',
      '--disable-features=TranslateUI',
      '--disable-features=site-per-process,Translate,BlinkGenPropertyTrees',
      '--disable-back-forward-cache'
    ]
  });

  const context = await browser.newContext({
    // 设置真实用户代理
    userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    // 设置视口尺寸
    viewport: { width: 1920, height: 1080 },
    // 设置时区
    timezoneId: 'Asia/Shanghai',
    // 设置语言
    locale: 'zh-CN,zh;q=0.9,en;q=0.8',
    // 设置地理信息
    geolocation: { longitude: 121.4737, latitude: 31.2304 },
    permissions: ['geolocation']
  });

  const page = await context.newPage();

  try {
    // 设置一些额外的头部信息
    await page.setExtraHTTPHeaders({
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
      'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
      'Accept-Encoding': 'gzip, deflate, br',
      'Connection': 'keep-alive',
      'Upgrade-Insecure-Requests': '1',
      'Sec-Fetch-Dest': 'document',
      'Sec-Fetch-Mode': 'navigate',
      'Sec-Fetch-Site': 'none',
      'Cache-Control': 'max-age=0'
    });

    // 访问页面
    console.log(`正在访问: ${url}`);
    const response = await page.goto(url, { 
      waitUntil: 'domcontentloaded',
      timeout: 30000 
    });

    // 检查响应状态
    if (response.status() !== 200 && response.status() !== 304) {
      console.log(`警告: 页面返回状态码 ${response.status()}`);
    }

    // 等待关键元素出现或一定时间，模拟人类行为
    try {
      // 尝试等待可能的推文内容元素出现
      await Promise.race([
        page.waitForSelector('[data-testid="tweetText"]', { timeout: 10000 }),
        page.waitForSelector('article[role="article"]', { timeout: 10000 }),
        page.waitForTimeout(10000) // 最多等待10秒
      ]);
    } catch (e) {
      console.log('提示: 未找到预期的元素，继续执行...');
    }

    // 注入脚本来隐藏自动化特征
    await page.addInitScript(() => {
      Object.defineProperty(navigator, 'webdriver', {
        get: () => undefined,
      });
      
      // 修改plugins属性
      Object.defineProperty(navigator, 'plugins', {
        get: () => ({
          length: 3,
          0: { filename: 'internal-pdf-viewer' },
          1: { filename: 'adsfk-plugin' },
          2: { filename: 'internal-nacl-plugin' },
          refresh: () => {},
        }),
      });
      
      // 修改languages属性
      Object.defineProperty(navigator, 'languages', {
        get: () => ['zh-CN', 'zh', 'en'],
      });
    });

    // 尝试多种方式来获取内容
    let content = '';
    let title = '';

    // 方法1: 尝试获取页面标题
    title = await page.title();
    
    // 方法2: 尝试获取推文内容
    const selectors = [
      '[data-testid="tweetText"]',
      'article div[lang]',
      '[data-testid="tweet"] div[dir="auto"]',
      'div[role="link"] div[dir="auto"]',
      'div[data-testid="cellInnerDiv"] div[lang]',
      '.tweet-text',
      'p'
    ];

    for (const selector of selectors) {
      try {
        const elements = await page.$$(selector);
        for (const element of elements) {
          const text = await element.textContent();
          if (text && text.trim().length > content.length) {
            content = text.trim();
          }
        }
        if (content.length > 50) break; // 如果找到了足够的内容，就停止
      } catch (e) {
        continue;
      }
    }

    // 如果还是没有找到内容，尝试获取整个body文本
    if (!content) {
      content = await page.locator('body').textContent();
      // 过滤掉常见的非内容文本
      const filteredLines = content.split('\n')
        .filter(line => 
          line.length > 20 && 
          !line.toLowerCase().includes('javascript') &&
          !line.toLowerCase().includes('enable') &&
          !line.toLowerCase().includes('browser') &&
          !line.toLowerCase().includes('supported')
        );
      content = filteredLines.slice(0, 10).join('\n');
    }

    // 返回结果
    const result = {
      success: true,
      title: title || 'X Post',
      content: content || '未能提取到内容',
      url: url
    };

    console.log('提取结果:', result);
    await browser.close();
    return result;

  } catch (error) {
    console.error('错误:', error.message);
    await browser.close();
    return {
      success: false,
      error: error.message,
      url: url
    };
  }
}

// 如果直接运行此脚本
if (require.main === module) {
  const url = process.argv[2];
  if (!url) {
    console.log('用法: node x_content_scraper.js <X链接>');
    process.exit(1);
  }
  
  scrapeXContent(url).then(result => {
    console.log(JSON.stringify(result));
  });
}

module.exports = { scrapeXContent };