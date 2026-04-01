import { DashboardLayout } from "@/components/DashboardLayout";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Database, Download, RefreshCw } from "lucide-react";
import { StatCard } from "@/components/StatCard";

const tables = [
  { name: "users", records: "12,847", size: "24.3 MB", lastUpdated: "방금 전", status: "정상" },
  { name: "products", records: "5,432", size: "18.7 MB", lastUpdated: "5분 전", status: "정상" },
  { name: "orders", records: "89,210", size: "156.2 MB", lastUpdated: "1분 전", status: "정상" },
  { name: "logs", records: "1,245,890", size: "892.1 MB", lastUpdated: "실시간", status: "경고" },
  { name: "sessions", records: "3,421", size: "12.8 MB", lastUpdated: "30초 전", status: "정상" },
];

const DataPage = () => {
  return (
    <DashboardLayout title="데이터 관리">
      <div className="space-y-6">
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <StatCard title="총 테이블" value="14" icon={Database} />
          <StatCard title="총 레코드" value="1.35M" change="↑ 2.4% 오늘" changeType="positive" icon={Database} />
          <StatCard title="총 용량" value="1.1 GB" change="73% 사용 중" changeType="neutral" icon={Database} />
        </div>

        <Card>
          <CardHeader className="pb-3">
            <div className="flex items-center justify-between">
              <CardTitle className="text-base font-semibold">테이블 목록</CardTitle>
              <div className="flex gap-2">
                <Button variant="outline" size="sm" className="gap-1.5">
                  <RefreshCw className="h-3.5 w-3.5" />
                  새로고침
                </Button>
                <Button variant="outline" size="sm" className="gap-1.5">
                  <Download className="h-3.5 w-3.5" />
                  내보내기
                </Button>
              </div>
            </div>
          </CardHeader>
          <CardContent className="p-0">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>테이블 이름</TableHead>
                  <TableHead>레코드 수</TableHead>
                  <TableHead>용량</TableHead>
                  <TableHead>마지막 업데이트</TableHead>
                  <TableHead>상태</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {tables.map((table) => (
                  <TableRow key={table.name} className="cursor-pointer">
                    <TableCell className="font-mono text-sm font-medium">{table.name}</TableCell>
                    <TableCell>{table.records}</TableCell>
                    <TableCell className="text-muted-foreground">{table.size}</TableCell>
                    <TableCell className="text-muted-foreground">{table.lastUpdated}</TableCell>
                    <TableCell>
                      <Badge
                        variant={table.status === "정상" ? "default" : "secondary"}
                        className="text-xs"
                      >
                        {table.status}
                      </Badge>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </CardContent>
        </Card>
      </div>
    </DashboardLayout>
  );
};

export default DataPage;
