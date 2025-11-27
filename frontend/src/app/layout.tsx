import './globals.css'
import type { Metadata, Viewport } from 'next'

export const metadata: Metadata = {
  title: 'Clima Cana - Informações Climáticas para Agricultores',
  description: 'Aplicação para fornecer informações climáticas relevantes para produtores de cana-de-açúcar',
}

export const viewport: Viewport = {
  width: 'device-width',
  initialScale: 1,
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="pt-BR">
      <head>
        <link rel="icon" href="/favicon.ico" />
        <meta name="theme-color" content="#2E7D32" />
      </head>
      <body className="min-h-screen bg-gradient-to-b from-green-50 to-white">
        <div className="min-h-screen flex flex-col">
          <header className="bg-primary-600 text-white shadow-lg">
            <div className="container mx-auto px-4 py-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <div className="text-2xl">🌾</div>
                  <div>
                    <h1 className="text-xl font-bold">Clima Cana</h1>
                    <p className="text-xs text-green-100">Informações climáticas para sua lavoura</p>
                  </div>
                </div>
                <div className="hidden sm:block">
                  <span className="text-sm bg-green-700 px-3 py-1 rounded-full">
                    🌱 Agricultura Inteligente
                  </span>
                </div>
              </div>
            </div>
          </header>
          
          <main className="flex-1 container mx-auto px-4 py-8">
            {children}
          </main>
          
          <footer className="bg-gray-100 border-t border-gray-200 mt-auto">
            <div className="container mx-auto px-4 py-6">
              <div className="text-center text-gray-600 text-sm">
                <p>© 2023 Clima Cana - Desenvolvido para produtores rurais</p>
                <p className="mt-1">Dados climáticos fornecidos por Open-Meteo</p>
              </div>
            </div>
          </footer>
        </div>
      </body>
    </html>
  )
}