import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Activity, AlertCircle, CheckCircle2, Clock } from "lucide-react"

// Mock data for demo
const TOTAL_CONTROLS = 24
const COMPLIANT = 18
const IN_PROGRESS = 4
const NON_COMPLIANT = 2

export function Dashboard() {
  return (
    <div className="container mx-auto py-10 px-4 md:px-8">
      {/* Hero Header */}
      <div className="mb-8 flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div>
          <h1 className="text-4xl md:text-5xl font-extrabold tracking-tight mb-2">Welcome to CloudTrust Inspector</h1>
          <p className="text-lg text-muted-foreground max-w-2xl">Your unified dashboard for compliance, evidence, and control management. Stay on top of your compliance posture with real-time insights and activity.</p>
        </div>
      </div>

      {/* Compliance Overview Cards */}
      <div className="grid gap-8 md:grid-cols-2 lg:grid-cols-4 mb-10">
        <Card className="transition-shadow hover:shadow-xl hover:-translate-y-1 duration-200">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-base font-semibold">Total Controls</CardTitle>
            <Activity className="h-6 w-6 text-primary" />
          </CardHeader>
          <CardContent>
            <div className="text-4xl font-extrabold tracking-tight mb-1">{TOTAL_CONTROLS}</div>
            <p className="text-sm text-muted-foreground">Across all frameworks</p>
          </CardContent>
        </Card>
        <Card className="transition-shadow hover:shadow-xl hover:-translate-y-1 duration-200">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-base font-semibold">Compliant</CardTitle>
            <CheckCircle2 className="h-6 w-6 text-green-500" />
          </CardHeader>
          <CardContent>
            <div className="text-4xl font-extrabold tracking-tight mb-1">{COMPLIANT}</div>
            <p className="text-sm text-muted-foreground">Controls in compliance</p>
          </CardContent>
        </Card>
        <Card className="transition-shadow hover:shadow-xl hover:-translate-y-1 duration-200">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-base font-semibold">Non-Compliant</CardTitle>
            <AlertCircle className="h-6 w-6 text-red-500" />
          </CardHeader>
          <CardContent>
            <div className="text-4xl font-extrabold tracking-tight mb-1">{NON_COMPLIANT}</div>
            <p className="text-sm text-muted-foreground">Controls requiring attention</p>
          </CardContent>
        </Card>
        <Card className="transition-shadow hover:shadow-xl hover:-translate-y-1 duration-200">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-base font-semibold">In Progress</CardTitle>
            <Clock className="h-6 w-6 text-yellow-500" />
          </CardHeader>
          <CardContent>
            <div className="text-4xl font-extrabold tracking-tight mb-1">{IN_PROGRESS}</div>
            <p className="text-sm text-muted-foreground">Controls being reviewed</p>
          </CardContent>
        </Card>
      </div>

      {/* Recent Activity */}
      <Card className="shadow-lg">
        <CardHeader>
          <CardTitle className="text-xl font-bold">Recent Activity</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4 min-h-[60px] flex items-center justify-center">
            <p className="text-base text-muted-foreground">No recent activity to display</p>
          </div>
        </CardContent>
      </Card>
    </div>
  )
} 