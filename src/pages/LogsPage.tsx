import { DashboardLayout } from "@/components/DashboardLayout";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Search, Filter } from "lucide-react";

const logs = [
  { id: 1, level: "INFO", message: "사용자 로그인 성공", source: "auth-service", timestamp: "2024-01-15 14:32:01" },
  { id: 2, level: "WARNING", message: "캐시 메모리 사용량 85% 초과", source: "cache-server", timestamp: "2024-01-15 14:31:45" },
  { id: 3, level: "ERROR", message: "외부 API 연결 타임아웃 (3000ms)", source: "api-gateway", timestamp: "2024-01-15 14:30:12" },
  { id: 4, level: "INFO", message: "배치 작업 'daily_report' 완료 (42s)", source: "scheduler", timestamp: "2024-01-15 14:28:00" },
  { id: 5, level: "INFO", message: "새 사용자 등록: user_0042", source: "user-service", timestamp: "2024-01-15 14:25:33" },
  { id: 6, level: "ERROR", message: "데이터베이스 쿼리 실패: timeout", source: "db-service", timestamp: "2024-01-15 14:22:10" },
  { id: 7, level: "INFO", message: "CDN 캐시 갱신 완료", source: "cdn-service", timestamp: "2024-01-15 14:20:00" },
  { id: 8, level: "WARNING", message: "Rate limit 임계값 도달: IP 192.168.1.45", source: "api-gateway", timestamp: "2024-01-15 14:18:22" },
];

const LogsPage = () => {
  return (
    <DashboardLayout title="활동 로그">
      <div className="space-y-6">
        <Card>
          <CardHeader className="pb-3">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
              <CardTitle className="text-base font-semibold">시스템 로그</CardTitle>
              <div className="flex items-center gap-3">
                <div className="relative">
                  <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                  <Input placeholder="로그 검색..." className="pl-9 h-9 w-56" />
                </div>
                <Button variant="outline" size="sm" className="gap-1.5">
                  <Filter className="h-3.5 w-3.5" />
                  필터
                </Button>
              </div>
            </div>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              {logs.map((log) => (
                <div
                  key={log.id}
                  className="flex items-start gap-3 p-3 rounded-lg bg-muted/30 hover:bg-muted/50 transition-colors"
                >
                  <Badge
                    variant={
                      log.level === "ERROR" ? "destructive" :
                      log.level === "WARNING" ? "secondary" : "outline"
                    }
                    className="mt-0.5 text-xs font-mono shrink-0 w-20 justify-center"
                  >
                    {log.level}
                  </Badge>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium">{log.message}</p>
                    <div className="flex items-center gap-3 mt-1">
                      <span className="text-xs text-muted-foreground font-mono">{log.source}</span>
                      <span className="text-xs text-muted-foreground">{log.timestamp}</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </DashboardLayout>
  );
};

export default LogsPage;
