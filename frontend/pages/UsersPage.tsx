import { DashboardLayout } from "@/components/DashboardLayout";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Search, Plus, MoreHorizontal } from "lucide-react";

const users = [
  { id: 1, name: "김민수", email: "minsu@example.com", role: "관리자", status: "활성", lastLogin: "2024-01-15" },
  { id: 2, name: "이지은", email: "jieun@example.com", role: "편집자", status: "활성", lastLogin: "2024-01-14" },
  { id: 3, name: "박서준", email: "seojun@example.com", role: "뷰어", status: "비활성", lastLogin: "2024-01-10" },
  { id: 4, name: "최유리", email: "yuri@example.com", role: "편집자", status: "활성", lastLogin: "2024-01-15" },
  { id: 5, name: "정태영", email: "taeyoung@example.com", role: "뷰어", status: "대기", lastLogin: "-" },
  { id: 6, name: "한소희", email: "sohee@example.com", role: "관리자", status: "활성", lastLogin: "2024-01-15" },
];

const UsersPage = () => {
  return (
    <DashboardLayout title="사용자 관리">
      <div className="space-y-6">
        <Card>
          <CardHeader className="pb-3">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
              <CardTitle className="text-base font-semibold">사용자 목록</CardTitle>
              <div className="flex items-center gap-3">
                <div className="relative">
                  <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                  <Input placeholder="사용자 검색..." className="pl-9 h-9 w-56" />
                </div>
                <Button size="sm" className="gap-1.5">
                  <Plus className="h-4 w-4" />
                  추가
                </Button>
              </div>
            </div>
          </CardHeader>
          <CardContent className="p-0">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>이름</TableHead>
                  <TableHead>이메일</TableHead>
                  <TableHead>역할</TableHead>
                  <TableHead>상태</TableHead>
                  <TableHead>마지막 로그인</TableHead>
                  <TableHead className="w-10"></TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {users.map((user) => (
                  <TableRow key={user.id}>
                    <TableCell className="font-medium">{user.name}</TableCell>
                    <TableCell className="text-muted-foreground">{user.email}</TableCell>
                    <TableCell>
                      <Badge variant={user.role === "관리자" ? "default" : "secondary"} className="text-xs">
                        {user.role}
                      </Badge>
                    </TableCell>
                    <TableCell>
                      <div className="flex items-center gap-2">
                        <div
                          className={`h-2 w-2 rounded-full ${
                            user.status === "활성" ? "bg-[hsl(142,76%,36%)]" :
                            user.status === "비활성" ? "bg-muted-foreground" :
                            "bg-[hsl(38,92%,50%)]"
                          }`}
                        />
                        <span className="text-sm">{user.status}</span>
                      </div>
                    </TableCell>
                    <TableCell className="text-muted-foreground">{user.lastLogin}</TableCell>
                    <TableCell>
                      <Button variant="ghost" size="icon" className="h-8 w-8">
                        <MoreHorizontal className="h-4 w-4" />
                      </Button>
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

export default UsersPage;
