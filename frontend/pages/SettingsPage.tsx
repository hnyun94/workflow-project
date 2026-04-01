import { DashboardLayout } from "@/components/DashboardLayout";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Switch } from "@/components/ui/switch";
import { Separator } from "@/components/ui/separator";

const SettingsPage = () => {
  return (
    <DashboardLayout title="설정">
      <div className="max-w-2xl space-y-6">
        <Card>
          <CardHeader>
            <CardTitle className="text-base">일반 설정</CardTitle>
            <CardDescription>시스템의 기본 설정을 관리합니다.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="siteName">사이트 이름</Label>
              <Input id="siteName" defaultValue="My Admin Panel" />
            </div>
            <div className="space-y-2">
              <Label htmlFor="apiUrl">API Base URL</Label>
              <Input id="apiUrl" defaultValue="https://api.example.com/v1" className="font-mono text-sm" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="text-base">알림 설정</CardTitle>
            <CardDescription>알림 수신 방법을 설정합니다.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            {[
              { label: "이메일 알림", desc: "시스템 오류 발생 시 이메일로 알림을 받습니다.", default: true },
              { label: "슬랙 알림", desc: "중요 이벤트를 슬랙 채널에 전송합니다.", default: false },
              { label: "브라우저 알림", desc: "브라우저 푸시 알림을 활성화합니다.", default: true },
            ].map((item, i) => (
              <div key={i}>
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium">{item.label}</p>
                    <p className="text-xs text-muted-foreground">{item.desc}</p>
                  </div>
                  <Switch defaultChecked={item.default} />
                </div>
                {i < 2 && <Separator className="mt-4" />}
              </div>
            ))}
          </CardContent>
        </Card>

        <div className="flex justify-end">
          <Button>변경사항 저장</Button>
        </div>
      </div>
    </DashboardLayout>
  );
};

export default SettingsPage;
