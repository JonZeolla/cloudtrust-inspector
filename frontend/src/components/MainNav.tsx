import { Link, useLocation } from 'react-router-dom'
import { cn } from '@/lib/utils'

const navItems = [
  {
    title: 'Dashboard',
    href: '/',
  },
  {
    title: 'Controls',
    href: '/controls',
  },
  {
    title: 'Evidence',
    href: '/evidence',
  },
  {
    title: 'Reports',
    href: '/reports',
  },
]

export function MainNav() {
  const location = useLocation()

  return (
    <nav className="flex items-center space-x-6 lg:space-x-8">
      <Link to="/" className="flex items-center space-x-2">
        <span className="font-bold">CloudTrust Inspector</span>
      </Link>
      {navItems.map((item) => (
        <Link
          key={item.href}
          to={item.href}
          className={cn(
            'text-sm font-medium transition-colors hover:text-primary',
            location.pathname === item.href
              ? 'text-foreground'
              : 'text-muted-foreground'
          )}
        >
          {item.title}
        </Link>
      ))}
    </nav>
  )
} 