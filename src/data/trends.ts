export interface Trend {
  id: number
  title: string
  summary: string
  image: string
  category: string
  author: string
  date: string
  likes: number
  height: number
}

export const trendsData: Trend[] = [
  {
    id: 1,
    title: '2026春夏趋势：柔和力量感',
    summary: '本季最值得关注的五大流行趋势，从柔和色调到力量感剪裁',
    image: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=spring%20summer%202026%20fashion%20trend%20soft%20power%20pastel%20colors%20editorial&image_size=portrait_4_3',
    category: '秀场',
    author: '时尚编辑部',
    date: '2026-05-18',
    likes: 2341,
    height: 280,
  },
  {
    id: 2,
    title: '街拍精选：东京街头风格',
    summary: '探索东京原宿与表参道的独特街头时尚',
    image: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=tokyo%20street%20style%20harajuku%20fashion%20photography%20vibrant&image_size=portrait_4_3',
    category: '街拍',
    author: '街拍达人',
    date: '2026-05-17',
    likes: 1892,
    height: 350,
  },
  {
    id: 3,
    title: '必备单品：经典风衣的10种穿法',
    summary: '一件风衣玩转整个春季，从职场到周末全搞定',
    image: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=classic%20trench%20coat%20styling%20fashion%20editorial%20beige&image_size=portrait_4_3',
    category: '搭配',
    author: '搭配师小美',
    date: '2026-05-16',
    likes: 3120,
    height: 300,
  },
  {
    id: 4,
    title: '极简主义衣橱构建指南',
    summary: '用30件单品打造365天不重样的穿搭',
    image: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=minimalist%20wardrobe%20capsule%20collection%20neutral%20organized%20closet&image_size=portrait_4_3',
    category: '单品',
    author: '生活美学',
    date: '2026-05-15',
    likes: 2756,
    height: 260,
  },
  {
    id: 5,
    title: '巴黎时装周高光时刻',
    summary: '从Chanel到Dior，盘点本季最令人难忘的秀场瞬间',
    image: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=paris%20fashion%20week%20runway%20haute%20couture%20glamour&image_size=portrait_4_3',
    category: '秀场',
    author: '时装周报道',
    date: '2026-05-14',
    likes: 4210,
    height: 340,
  },
  {
    id: 6,
    title: '运动风也能很时髦',
    summary: 'Athleisure穿搭进阶，运动与时尚的完美融合',
    image: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=athleisure%20fashion%20sporty%20chic%20outfit%20modern%20styling&image_size=portrait_4_3',
    category: '搭配',
    author: '运动时尚',
    date: '2026-05-13',
    likes: 1567,
    height: 290,
  },
  {
    id: 7,
    title: '配饰的力量：小物件大改变',
    summary: '如何用配饰为基本款穿搭注入灵魂',
    image: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=fashion%20accessories%20jewelry%20bags%20styling%20elegant%20editorial&image_size=portrait_4_3',
    category: '单品',
    author: '配饰控',
    date: '2026-05-12',
    likes: 2089,
    height: 320,
  },
  {
    id: 8,
    title: '首尔街头：K-Fashion灵感',
    summary: '韩系穿搭的精髓，简约中见巧思',
    image: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=korean%20fashion%20seoul%20street%20style%20minimalist%20chic&image_size=portrait_4_3',
    category: '街拍',
    author: '韩风追踪',
    date: '2026-05-11',
    likes: 3456,
    height: 310,
  },
]

export const categories = ['全部', '街拍', '秀场', '搭配', '单品']

export const hotTopics = [
  '#春日穿搭',
  '#极简风',
  '#法式优雅',
  '#运动时尚',
  '#复古回潮',
  '#职场穿搭',
  '#约会look',
  '#色彩搭配',
]
