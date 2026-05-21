export interface Outfit {
  id: number
  title: string
  description: string
  image: string
  tags: string[]
  scene: string
  style: string
  rating: number
  items: { name: string; brand: string; price: string }[]
}

export const outfitsData: Outfit[] = [
  {
    id: 1,
    title: '都市通勤优雅风',
    description: '简约而不简单的通勤搭配，展现职场女性的干练与优雅',
    image: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=elegant%20business%20woman%20outfit%20minimalist%20fashion%20photography%20soft%20lighting&image_size=portrait_4_3',
    tags: ['通勤', '优雅', '简约'],
    scene: 'commute',
    style: 'elegant',
    rating: 4.8,
    items: [
      { name: '修身西装外套', brand: 'COS', price: '¥1,290' },
      { name: '丝质衬衫', brand: 'Massimo Dutti', price: '¥690' },
      { name: '高腰阔腿裤', brand: 'COS', price: '¥890' },
    ],
  },
  {
    id: 2,
    title: '周末休闲随性搭',
    description: '轻松自在的周末穿搭，舒适与时尚兼得',
    image: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=casual%20weekend%20outfit%20street%20style%20fashion%20photography%20natural%20light&image_size=portrait_4_3',
    tags: ['休闲', '随性', '舒适'],
    scene: 'casual',
    style: 'casual',
    rating: 4.6,
    items: [
      { name: 'oversized卫衣', brand: 'A.P.C.', price: '¥980' },
      { name: '直筒牛仔裤', brand: 'Levi\'s', price: '¥599' },
      { name: '小白鞋', brand: 'Common Projects', price: '¥2,400' },
    ],
  },
  {
    id: 3,
    title: '浪漫约会甜美风',
    description: '温柔浪漫的约会穿搭，让他一见倾心',
    image: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=romantic%20date%20outfit%20feminine%20dress%20fashion%20photography%20soft%20pink&image_size=portrait_4_3',
    tags: ['约会', '甜美', '浪漫'],
    scene: 'date',
    style: 'sweet',
    rating: 4.9,
    items: [
      { name: '碎花连衣裙', brand: 'Rouje', price: '¥1,580' },
      { name: '针织开衫', brand: 'Maje', price: '¥1,290' },
      { name: '玛丽珍鞋', brand: 'Repetto', price: '¥2,100' },
    ],
  },
  {
    id: 4,
    title: '运动活力街头风',
    description: '充满活力的运动街头穿搭，释放你的能量',
    image: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=sporty%20street%20style%20outfit%20athleisure%20fashion%20photography%20dynamic&image_size=portrait_4_3',
    tags: ['运动', '活力', '街头'],
    scene: 'sport',
    style: 'street',
    rating: 4.5,
    items: [
      { name: '运动背心', brand: 'Lululemon', price: '¥550' },
      { name: '束脚运动裤', brand: 'Nike', price: '¥699' },
      { name: '老爹鞋', brand: 'Balenciaga', price: '¥6,900' },
    ],
  },
  {
    id: 5,
    title: '法式复古优雅风',
    description: '经典法式穿搭，永恒的优雅与浪漫',
    image: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=french%20vintage%20elegant%20outfit%20parisian%20chic%20fashion%20photography&image_size=portrait_4_3',
    tags: ['法式', '复古', '优雅'],
    scene: 'date',
    style: 'vintage',
    rating: 4.7,
    items: [
      { name: '风衣外套', brand: 'Burberry', price: '¥15,900' },
      { name: '条纹衫', brand: 'Saint James', price: '¥780' },
      { name: '乐福鞋', brand: 'G.H.Bass', price: '¥1,200' },
    ],
  },
  {
    id: 6,
    title: '极简主义高级感',
    description: '少即是多，用最简单的单品穿出高级感',
    image: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=minimalist%20luxury%20outfit%20neutral%20tones%20fashion%20photography%20clean&image_size=portrait_4_3',
    tags: ['极简', '高级', '中性'],
    scene: 'commute',
    style: 'minimal',
    rating: 4.8,
    items: [
      { name: '羊绒毛衣', brand: 'The Row', price: '¥5,800' },
      { name: '西装裤', brand: 'Lemaire', price: '¥3,200' },
      { name: '手提包', brand: 'Bottega Veneta', price: '¥12,500' },
    ],
  },
]

export const scenes = [
  { key: 'commute', label: '通勤', icon: 'Briefcase' },
  { key: 'date', label: '约会', icon: 'Heart' },
  { key: 'casual', label: '休闲', icon: 'Coffee' },
  { key: 'sport', label: '运动', icon: 'Dumbbell' },
  { key: 'party', label: '派对', icon: 'PartyPopper' },
  { key: 'travel', label: '旅行', icon: 'Plane' },
]

export const styles = [
  { key: 'elegant', label: '优雅' },
  { key: 'casual', label: '休闲' },
  { key: 'sweet', label: '甜美' },
  { key: 'street', label: '街头' },
  { key: 'vintage', label: '复古' },
  { key: 'minimal', label: '极简' },
]
