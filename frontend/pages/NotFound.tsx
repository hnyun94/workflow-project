import { useLocation } from "react-router-dom";
import { useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Home } from "lucide-react";

const NotFound = () => {
  const location = useLocation();

  useEffect(() => {
    console.error("404 Error: User attempted to access non-existent route:", location.pathname);
  }, [location.pathname]);

  return (
    <div className="flex min-h-screen items-center justify-center bg-background">
      <div className="text-center space-y-4">
        <div className="text-7xl font-bold text-primary">404</div>
        <h1 className="text-xl font-semibold text-foreground">페이지를 찾을 수 없습니다</h1>
        <p className="text-muted-foreground">요청하신 페이지가 존재하지 않거나 이동되었습니다.</p>
        <Button asChild className="gap-2 mt-2">
          <a href="/">
            <Home className="h-4 w-4" />
            홈으로 돌아가기
          </a>
        </Button>
      </div>
    </div>
  );
};

export default NotFound;
