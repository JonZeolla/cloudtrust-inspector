import { Link, useLocation } from "react-router-dom"
import { cn } from "@/lib/utils"

const items = [
  {
    title: "Dashboard",
    href: "/",
  },
  {
    title: "Controls",
    href: "/controls",
  },
  {
    title: "Evidence",
    href: "/evidence",
  },
  {
    title: "Reports",
    href: "/reports",
  },
]

export function MainNav() {
  const location = useLocation()

  return (
    <div className="mr-4 hidden md:flex">
      <Link to="/" className="mr-6 flex items-center space-x-2">
        <span className="hidden font-bold sm:inline-block">
          CloudTrust Inspector
        </span>
      </Link>
      <nav className="flex items-center space-x-6 text-sm font-medium">
        {items.map((item) => (
          <Link
            key={item.href}
            to={item.href}
            className={cn(
              "transition-colors hover:text-foreground/80",
              location.pathname === item.href
                ? "text-foreground"
                : "text-foreground/60"
            )}
          >
            {item.title}
          </Link>
        ))}
      </nav>
    </div>
  )
} 