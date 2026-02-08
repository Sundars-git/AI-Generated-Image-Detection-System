import "./globals.css";

export const metadata = {
  title: "AI Image Detector",
  description: "Detect AI-generated images vs Real photos",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
