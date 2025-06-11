import type { Flow, OldTransaction, Profile, Report } from '@/models/type';

const profile: Profile = {
  name: '藤崎 剛暉',
  title: '自由民主党',
  party: '自由民主党',
  district: '東京都墨田区',
  image: '/demo-kokifujisaki.jpg',
};

const reports: Report[] = [
  {
    id: 'demo-koki-fujisaki-2024', // ファイル名からIDを生成
    totalIncome: 2154820,
    totalExpense: 1143920,
    totalBalance: 1010900,
    year: 2024,
    orgType: '政党の支部',
    orgName: '自由民主党東京都墨田区第十六支部',
    activityArea: '東京都内',
    representative: '藤崎 剛暉',
    fundManagementOrg: '無し',
    accountingManager: '前田 隆',
    administrativeManager: '藤崎 剛暉',
    lastUpdate: '2024年3月30日',
  },
  {
    id: 'demo-koki-fujisaki-2023', // ファイル名からIDを生成
    totalIncome: 607500,
    totalExpense: 250000,
    totalBalance: 357500,
    year: 2023,
    orgType: '政党の支部',
    orgName: '自由民主党東京都墨田区第十六支部',
    activityArea: '東京都内',
    representative: '藤崎 剛暉',
    fundManagementOrg: '無し',
    accountingManager: '前田 隆',
    administrativeManager: '藤崎 剛暉',
    lastUpdate: '2023年3月30日',
  },
  {
    id: 'demo-koki-fujisaki-2022', // ファイル名からIDを生成
    totalIncome: 494300, //
    totalExpense: 120000, //
    totalBalance: 374300, //
    year: 2022, //
    orgType: '政党の支部', //
    orgName: '自由民主党東京都墨田区第十六支部', //
    activityArea: '東京都内', //
    representative: '藤崎 剛暉', //
    fundManagementOrg: '無し', //
    accountingManager: '前田 隆', //
    administrativeManager: '藤崎 剛暉', //
    lastUpdate: '2022年3月27日', //
  },
];

const report = reports[0];

const flowsByYear: Record<number, Flow[]> = {
  2022: [
    // 収入
    {
      id: 'i1',
      name: '前年からの繰越額',
      direction: 'income',
      value: 272300, //
      parent: '総収入',
    },
    {
      id: 'i2',
      name: '本年の収入額',
      direction: 'income',
      value: 222000, //
      parent: '総収入',
    },
    {
      id: 'i3',
      name: '個人の負担する党費又は会費',
      direction: 'income',
      value: 22000, //
      parent: '本年の収入額',
    },
    {
      id: 'i4',
      name: '本部又は支部から供与された交付金',
      direction: 'income',
      value: 200000, //
      parent: '本年の収入額',
    },
    // 総収入
    {
      id: 'i_total',
      name: '総収入',
      direction: 'expense',
      value: 494300, //
      parent: null,
    },
    // 支出
    {
      id: 'e2',
      name: '政治活動費',
      direction: 'expense',
      value: 120000, //
      parent: '総収入',
    },
    {
      id: 'e3',
      name: '組織活動費',
      direction: 'expense',
      value: 120000, //
      parent: '政治活動費',
    },
    // 翌年への繰越
    {
      id: 'e_next',
      name: '翌年への繰越',
      direction: 'expense',
      value: 374300, //
      parent: '総収入',
    },
  ],
  2023: [
    // --- 2023年の更新データ開始 ---
    // 収入
    {
      id: 'i1',
      name: '前年からの繰越額',
      direction: 'income',
      value: 374300, //
      parent: '総収入',
    },
    {
      id: 'i2',
      name: '本年の収入額',
      direction: 'income',
      value: 233200, //
      parent: '総収入',
    },
    {
      id: 'i3',
      name: '個人の負担する党費又は会費',
      direction: 'income',
      value: 33200, //
      parent: '本年の収入額',
    },
    {
      id: 'i4',
      name: '本部又は支部から供与された交付金',
      direction: 'income',
      value: 200000, //
      parent: '本年の収入額',
    },
    // 総収入
    {
      id: 'i_total',
      name: '総収入',
      direction: 'expense',
      value: 607500, //
      parent: null,
    },
    // 支出
    {
      id: 'e2',
      name: '政治活動費',
      direction: 'expense',
      value: 250000, //
      parent: '総収入',
    },
    {
      id: 'e3',
      name: '組織活動費',
      direction: 'expense',
      value: 250000, //
      parent: '政治活動費',
    },
    // 翌年への繰越
    {
      id: 'e_next',
      name: '翌年への繰越',
      direction: 'expense',
      value: 357500, //
      parent: '総収入',
    },
  ],
  2024: [
    // --- 2024年の更新データ開始 ---
    // 収入
    {
      id: 'i1',
      name: '前年からの繰越額',
      direction: 'income',
      value: 357500, //
      parent: '総収入',
    },
    {
      id: 'i2',
      name: '本年の収入額',
      direction: 'income',
      value: 1797320, //
      parent: '総収入',
    },
    {
      id: 'i3',
      name: '個人の負担する党費又は会費',
      direction: 'income',
      value: 28400, //
      parent: '本年の収入額',
    },
    {
      id: 'i4',
      name: '寄附',
      direction: 'income',
      value: 1468920, //
      parent: '本年の収入額',
    },
    {
      id: 'i5',
      name: '本部又は支部から供与された交付金',
      direction: 'income',
      value: 300000, //
      parent: '本年の収入額',
    },
    {
      id: 'i_total',
      name: '総収入',
      direction: 'expense',
      value: 2154820, //
      parent: null,
    },
    // 支出
    {
      id: 'e2',
      name: '政治活動費',
      direction: 'expense',
      value: 1143920, //
      parent: '総収入',
    },
    {
      id: 'e3',
      name: '選挙関係費',
      direction: 'expense',
      value: 1100000, //
      parent: '政治活動費',
    },
    {
      id: 'e4',
      name: 'その他の経費',
      direction: 'expense',
      value: 43920, //
      parent: '政治活動費',
    },
    // 翌年への繰越
    {
      id: 'e_next',
      name: '翌年への繰越',
      direction: 'expense',
      value: 1010900, //
      parent: '総収入',
    },
  ],
};

// 後方互換性のため、デフォルトでは2022年のデータを使用
const flows: Flow[] = flowsByYear[2022];

const incomeTransactionsByYear: Record<number, OldTransaction[]> = {
  2022: [
    {
      id: 'i1',
      name: '前年からの繰越額',
      date: '2022/1/1',
      category: '前年繰越',
      value: 272300, //
      percentage: +((272300 / 494300) * 100).toFixed(1),
    },
    {
      id: 'i2',
      name: '個人の負担する党費又は会費',
      date: '2022/12/31',
      category: '党費・会費',
      value: 22000, //
      percentage: +((22000 / 494300) * 100).toFixed(1),
    },
    {
      id: 'i3',
      name: '本部又は支部から供与された交付金',
      date: '2022/12/31',
      category: '交付金',
      value: 200000, //
      percentage: +((200000 / 494300) * 100).toFixed(1),
    },
  ],
  2023: [
    // --- 2023年の更新データ開始 ---
    {
      id: 'i1',
      name: '前年からの繰越額',
      date: '2023/1/1',
      category: '前年繰越',
      value: 374300, //
      percentage: +((374300 / 607500) * 100).toFixed(1),
    },
    {
      id: 'i2',
      name: '個人の負担する党費又は会費',
      date: '2023/12/31',
      category: '党費・会費',
      value: 33200, //
      percentage: +((33200 / 607500) * 100).toFixed(1),
    },
    {
      id: 'i3',
      name: '本部又は支部から供与された交付金',
      date: '2023/12/31',
      category: '交付金',
      value: 200000, //
      percentage: +((200000 / 607500) * 100).toFixed(1),
    },
  ],
  2024: [
    // --- 2024年の更新データ開始 ---
    {
      id: 'i1',
      name: '前年からの繰越額',
      date: '2024/1/1',
      category: '前年繰越',
      value: 357500, //
      percentage: +((357500 / 2154820) * 100).toFixed(1),
    },
    {
      id: 'i2',
      name: '個人の負担する党費又は会費',
      date: '2024/12/31',
      category: '党費・会費',
      value: 28400, //
      percentage: +((28400 / 2154820) * 100).toFixed(1),
    },
    {
      id: 'i3',
      name: '寄附',
      date: '2024/12/31',
      category: '寄附',
      value: 1468920, //
      percentage: +((1468920 / 2154820) * 100).toFixed(1),
    },
    {
      id: 'i4',
      name: '本部又は支部から供与された交付金',
      date: '2024/12/31',
      category: '交付金',
      value: 300000, //
      percentage: +((300000 / 2154820) * 100).toFixed(1),
    },
  ],
};

// 後方互換性のため、デフォルトでは2022年のデータを使用
const incomeTransactions: OldTransaction[] = incomeTransactionsByYear[2022];

const expenseTransactionsByYear: Record<number, OldTransaction[]> = {
  2022: [
    // {
    //   id: 'e1',
    //   name: '人件費',
    //   date: '2022/12/31',
    //   category: '経常経費',
    //   value: 0, //
    //   percentage: 0,
    // },
    // {
    //   id: 'e2',
    //   name: '光熱水費',
    //   date: '2022/12/31',
    //   category: '経常経費',
    //   value: 0, //
    //   percentage: 0,
    // },
    // {
    //   id: 'e3',
    //   name: '備品・消耗品費',
    //   date: '2022/12/31',
    //   category: '経常経費',
    //   value: 0, //
    //   percentage: 0,
    // },
    // {
    //   id: 'e4',
    //   name: '事務所費',
    //   date: '2022/12/31',
    //   category: '経常経費',
    //   value: 0, //
    //   percentage: 0,
    // },
    {
      id: 'e5',
      name: '組織活動費',
      date: '2022/12/31',
      category: '政治活動費',
      value: 120000, //
      percentage: +((120000 / 120000) * 100).toFixed(1),
    },
    // {
    //   id: 'e6',
    //   name: '選挙関係費',
    //   date: '2022/12/31',
    //   category: '政治活動費',
    //   value: 0, //
    //   percentage: 0,
    // },
    // {
    //   id: 'e7',
    //   name: '機関紙誌の発行その他の事業費',
    //   date: '2022/12/31',
    //   category: '政治活動費',
    //   value: 0, //
    //   percentage: 0,
    // },
    // {
    //   id: 'e8',
    //   name: '調査研究費',
    //   date: '2022/12/31',
    //   category: '政治活動費',
    //   value: 0, //
    //   percentage: 0,
    // },
    // {
    //   id: 'e9',
    //   name: '寄附・交付金',
    //   date: '2022/12/31',
    //   category: '政治活動費',
    //   value: 0, //
    //   percentage: 0,
    // },
    // {
    //   id: 'e10',
    //   name: 'その他の経費',
    //   date: '2022/12/31',
    //   category: '政治活動費',
    //   value: 0, //
    //   percentage: 0,
    // },
  ],
  2023: [
    // {
    //   id: 'e1',
    //   name: '人件費',
    //   date: '2023/12/31',
    //   category: '経常経費',
    //   value: 0,
    //   percentage: 0,
    // },
    // {
    //   id: 'e2',
    //   name: '光熱水費',
    //   date: '2023/12/31',
    //   category: '経常経費',
    //   value: 0,
    //   percentage: 0,
    // },
    // {
    //   id: 'e3',
    //   name: '備品・消耗品費',
    //   date: '2023/12/31',
    //   category: '経常経費',
    //   value: 0,
    //   percentage: 0,
    // },
    // {
    //   id: 'e4',
    //   name: '事務所費',
    //   date: '2023/12/31',
    //   category: '経常経費',
    //   value: 0,
    //   percentage: 0,
    // },
    {
      id: 'e5',
      name: '組織活動費',
      date: '2023/12/31',
      category: '政治活動費',
      value: 250000, //
      percentage: +((250000 / 250000) * 100).toFixed(1),
    },
    // {
    //   id: 'e6',
    //   name: '選挙関係費',
    //   date: '2023/12/31',
    //   category: '政治活動費',
    //   value: 0,
    //   percentage: 0,
    // },
    // {
    //   id: 'e7',
    //   name: '機関紙誌の発行その他の事業費',
    //   date: '2023/12/31',
    //   category: '政治活動費',
    //   value: 0,
    //   percentage: 0,
    // },
    // {
    //   id: 'e8',
    //   name: '調査研究費',
    //   date: '2023/12/31',
    //   category: '政治活動費',
    //   value: 0,
    //   percentage: 0,
    // },
    // {
    //   id: 'e9',
    //   name: '寄附・交付金',
    //   date: '2023/12/31',
    //   category: '政治活動費',
    //   value: 0,
    //   percentage: 0,
    // },
    // {
    //   id: 'e10',
    //   name: 'その他の経費',
    //   date: '2023/12/31',
    //   category: '政治活動費',
    //   value: 0,
    //   percentage: 0,
    // },
  ],
  2024: [
    // --- 2024年の更新データ開始 ---
    // {
    //   id: 'e1',
    //   name: '人件費',
    //   date: '2024/12/31',
    //   category: '経常経費',
    //   value: 0, //
    //   percentage: 0,
    // },
    // {
    //   id: 'e2',
    //   name: '光熱水費',
    //   date: '2024/12/31',
    //   category: '経常経費',
    //   value: 0, //
    //   percentage: 0,
    // },
    // {
    //   id: 'e3',
    //   name: '備品・消耗品費',
    //   date: '2024/12/31',
    //   category: '経常経費',
    //   value: 0, //
    //   percentage: 0,
    // },
    // {
    //   id: 'e4',
    //   name: '事務所費',
    //   date: '2024/12/31',
    //   category: '経常経費',
    //   value: 0, //
    //   percentage: 0,
    // },
    // {
    //   id: 'e5',
    //   name: '組織活動費',
    //   date: '2024/12/31',
    //   category: '政治活動費',
    //   value: 0, //
    //   percentage: 0,
    // },
    {
      id: 'e6',
      name: '選挙関係費',
      date: '2024/12/31',
      category: '政治活動費',
      value: 1100000, //
      percentage: +((1100000 / 1143920) * 100).toFixed(1),
    },
    // {
    //   id: 'e7',
    //   name: '機関紙誌の発行その他の事業費',
    //   date: '2024/12/31',
    //   category: '政治活動費',
    //   value: 0, //
    //   percentage: 0,
    // },
    // {
    //   id: 'e8',
    //   name: '調査研究費',
    //   date: '2024/12/31',
    //   category: '政治活動費',
    //   value: 0, //
    //   percentage: 0,
    // },
    // {
    //   id: 'e9',
    //   name: '寄附・交付金',
    //   date: '2024/12/31',
    //   category: '政治活動費',
    //   value: 0, //
    //   percentage: 0,
    // },
    {
      id: 'e10',
      name: 'その他の経費',
      date: '2024/12/31',
      category: '政治活動費',
      value: 43920, //
      percentage: +((43920 / 1143920) * 100).toFixed(1),
    },
  ],
};

// 後方互換性のため、デフォルトでは2022年のデータを使用
const expenseTransactions: OldTransaction[] = expenseTransactionsByYear[2022];

// 年度に応じたデータを取得する関数
export const getDataByYear = (year: number) => {
  const reportForYear = reports.find((r) => r.year === year) || reports[0];

  return {
    id: reportForYear.id,
    profile,
    report: reportForYear,
    reports,
    flows: flowsByYear[year] || flowsByYear[2022],
    incomeTransactions:
      incomeTransactionsByYear[year] || incomeTransactionsByYear[2022],
    expenseTransactions:
      expenseTransactionsByYear[year] || expenseTransactionsByYear[2022],
    // 年度別データへのアクセス
    flowsByYear,
    incomeTransactionsByYear,
    expenseTransactionsByYear,
  };
};

// URLパスから年度を抽出してデータを取得する関数
export const getDataByPath = (path: string) => {
  const yearMatch = path.match(/(\d{4})/);
  const year = yearMatch ? Number.parseInt(yearMatch[1]) : 2022;
  return getDataByYear(year);
};

export default {
  id: report.id,
  profile,
  report,
  reports,
  flows,
  incomeTransactions,
  expenseTransactions,
  // 年度別データへのアクセス
  flowsByYear,
  incomeTransactionsByYear,
  expenseTransactionsByYear,
  // 動的データ取得関数
  getDataByYear,
  getDataByPath,
};
