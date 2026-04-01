import { DashboardLayout } from "@/components/DashboardLayout";
import { StatCard } from "@/components/StatCard";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Users, Database, Activity, Server, ArrowUpRight, ArrowDownRight } from "lucide-react";

const recentActivities = [
  { id: 1, action: "사용자 생성", user: "admin", target: "user_0042", time: "2분 전", status: "성공" },
  { id: 2, action: "데이터 업데이트", user: "system", target: "products", time: "5분 전", status: "성공" },
  { id: 3, action: "API 호출 실패", user: "api_bot", target: "/api/v1/sync", time: "12분 전", status: "실패" },
  { id: 4, action: "배치 작업 완료", user: "scheduler", target: "daily_report", time: "30분 전", status: "성공" },
  { id: 5, action: "로그인 시도", user: "unknown", target: "auth", time: "1시간 전", status: "차단" },
];

const systemStatus = [
  { name: "API 서버", status: "정상", uptime: "99.9%" },
  { name: "데이터베이스", status: "정상", uptime: "99.8%" },
  { name: "캐시 서버", status: "경고", uptime: "98.2%" },
  { name: "큐 워커", status: "정상", uptime: "99.7%" },
];

const Index = () => {
  return (
    <DashboardLayout title="대시보드">
      <div className="space-y-6">
        {/* Stats Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <StatCard
            title="총 사용자"
            value="12,847"
            change="↑ 12% 지난 달 대비"
            changeType="positive"
            icon={Users}
          />
          <StatCard
            title="데이터 레코드"
            value="1.2M"
            change="↑ 8% 지난 주 대비"
            changeType="positive"
            icon={Database}
          />
          <StatCard
            title="API 요청/분"
            value="3,421"
            change="↓ 3% 어제 대비"
            changeType="negative"
            icon={Activity}
          />
          <StatCard
            title="서버 상태"
            value="98.5%"
            change="정상 가동 중"
            changeType="neutral"
            icon={Server}
          />
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Recent Activity */}
          <Card className="lg:col-span-2">
            <CardHeader className="pb-3">
              <CardTitle className="text-base font-semibold">최근 활동</CardTitle>
            </CardHeader>
            <CardContent className="p-0">
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>작업</TableHead>
                    <TableHead>사용자</TableHead>
                    <TableHead>대상</TableHead>
                    <TableHead>시간</TableHead>
                    <TableHead>상태</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {recentActivities.map((activity) => (
                    <TableRow key={activity.id}>
                      <TableCell className="font-medium">{activity.action}</TableCell>
                      <TableCell className="text-muted-foreground">{activity.user}</TableCell>
                      <TableCell className="font-mono text-xs text-muted-foreground">{activity.target}</TableCell>
                      <TableCell className="text-muted-foreground">{activity.time}</TableCell>
                      <TableCell>
                        <Badge
                          variant={
                            activity.status === "성공" ? "default" :
                            activity.status === "실패" ? "destructive" : "secondary"
                          }
                          className="text-xs"
                        >
                          {activity.status}
                        </Badge>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </CardContent>
          </Card>

          {/* System Status */}
          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="text-base font-semibold">시스템 상태</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {systemStatus.map((system) => (
                  <div
                    key={system.name}
                    className="flex items-center justify-between p-3 rounded-lg bg-muted/50"
                  >
                    <div className="flex items-center gap-3">
                      <div
                        className={`h-2.5 w-2.5 rounded-full ${
                          system.status === "정상"
                            ? "bg-[hsl(142,76%,36%)]"
                            : "bg-[hsl(38,92%,50%)]"
                        }`}
                      />
                      <span className="text-sm font-medium">{system.name}</span>
                    </div>
                    <span className="text-sm text-muted-foreground">{system.uptime}</span>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </DashboardLayout>
  );
};

export default Index;
