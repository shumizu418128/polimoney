import { Box } from '@chakra-ui/react';
import type { Metadata } from 'next';
import { BoardMetadata } from '@/components/BoardMetadata';
import { BoardSummary } from '@/components/BoardSummary';
import { BoardTransactions } from '@/components/BoardTransactions';
import { Footer } from '@/components/Footer';
import { Header } from '@/components/Header';
import { Notice } from '@/components/Notice';
import data, { getDataByYear } from '@/data/demo-kokifujisaki';

export async function generateMetadata(): Promise<Metadata> {
  const yearData = getDataByYear(2023);
  return {
    title: `${yearData.profile.name} | Polimoney (ポリマネー)`,
  };
}

export default async function Page() {
  // 2023年のデータを取得
  const yearData = getDataByYear(2023);
  const reportData = yearData.datas[0];
  const allReports = data.datas.map((d) => d.report);

  return (
    <Box>
      <Header />
      <BoardSummary
        profile={yearData.profile}
        report={reportData.report}
        otherReports={allReports}
        flows={reportData.flows}
      />
      <BoardTransactions
        direction={'income'}
        total={reportData.report.totalIncome}
        transactions={reportData.transactions.filter(
          (t) => t.direction === 'income',
        )}
        showPurpose={false}
        showDate={false}
      />
      <BoardTransactions
        direction={'expense'}
        total={reportData.report.totalExpense}
        transactions={reportData.transactions.filter(
          (t) => t.direction === 'expense',
        )}
        showPurpose={false}
        showDate={false}
      />
      <BoardMetadata report={reportData.report} />
      <Notice />
      <Footer />
    </Box>
  );
}
