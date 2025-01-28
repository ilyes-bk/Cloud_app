import {
  Links,
  Meta,
  Outlet,
  Scripts,
  ScrollRestoration,
} from "@remix-run/react";
import { LoaderFunction } from "@remix-run/node";
import type { LinksFunction } from "@remix-run/node";
import { json } from "@remix-run/node";
import { isLoggedIn } from "./lib/authenticate";
import "./tailwind.css";
import { AuthProvider } from "./contexts/AuthContext";
import { ConversationProvider } from "./contexts/ConversationContext";
import { useLoaderData } from "@remix-run/react";
export const links: LinksFunction = () => [
  { rel: "preconnect", href: "https://fonts.googleapis.com" },
  {
    rel: "preconnect",
    href: "https://fonts.gstatic.com",
    crossOrigin: "anonymous",
  },
  {
    rel: "stylesheet",
    href: "https://fonts.googleapis.com/css2?family=Inter:ital,opsz,wght@0,14..32,100..900;1,14..32,100..900&display=swap",
  },
];
export const loader: LoaderFunction = async ({ request }) => {
  const url = new URL(request.url);
  const pathname = url.pathname; // Extract the pathname (e.g., "/about")

  // Check if the pathname includes "login"
  if (pathname.includes("login")) {
   return json({ payload: null }); // Return null if it's the login page
  }

  // Proceed with authentication for all other pages
  const payload = await isLoggedIn(request, true);

  // Return the authentication result as payload
  return json({ payload: payload });
};

export function Layout({ children }: { children: React.ReactNode }) {
  const { payload }: any = useLoaderData();
  return (
    <html lang="en">
      <head>
        <meta charSet="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <Meta />
        <Links />
      </head>
      <body>
        <AuthProvider user={payload}>
          <ConversationProvider>{children}</ConversationProvider>
        </AuthProvider>
        <ScrollRestoration />
        <Scripts />
      </body>
    </html>
  );
}

export default function App() {
  return <Outlet />;
}
