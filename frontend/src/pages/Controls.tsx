import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"

export function Controls() {
  return (
    <div className="container mx-auto py-10 px-4 md:px-8">
      {/* Hero Header */}
      <div className="mb-8 flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div>
          <h1 className="text-4xl md:text-5xl font-extrabold tracking-tight mb-2">Controls</h1>
          <p className="text-lg text-muted-foreground max-w-2xl">Manage your compliance frameworks, control status, and evidence in one place. Stay organized and audit-ready.</p>
        </div>
      </div>
      <div className="grid gap-8 md:grid-cols-2 lg:grid-cols-3">
        <Card className="transition-shadow hover:shadow-xl hover:-translate-y-1 duration-200">
          <CardHeader>
            <CardTitle className="text-lg font-semibold">Control Framework</CardTitle>
            <CardDescription>Select a compliance framework to view controls</CardDescription>
          </CardHeader>
          <CardContent>
            <p>Framework selection and control mapping will be implemented here.</p>
          </CardContent>
        </Card>
        <Card className="transition-shadow hover:shadow-xl hover:-translate-y-1 duration-200">
          <CardHeader>
            <CardTitle className="text-lg font-semibold">Control Status</CardTitle>
            <CardDescription>Overview of control implementation status</CardDescription>
          </CardHeader>
          <CardContent>
            <p>Control status tracking and metrics will be displayed here.</p>
          </CardContent>
        </Card>
        <Card className="transition-shadow hover:shadow-xl hover:-translate-y-1 duration-200">
          <CardHeader>
            <CardTitle className="text-lg font-semibold">Control Evidence</CardTitle>
            <CardDescription>Manage evidence for control implementation</CardDescription>
          </CardHeader>
          <CardContent>
            <p>Evidence collection and management features will be added here.</p>
          </CardContent>
        </Card>
      </div>
    </div>
  )
} 