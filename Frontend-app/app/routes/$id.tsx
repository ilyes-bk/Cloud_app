import {
  MetaFunction,
  useNavigate,
} from "@remix-run/react";
import { json, LoaderFunction } from "@remix-run/node";
import LeftSide from "~/components/pages/chat/LeftSide";
import RightSide from "~/components/pages/chat/RightSide";
import { isLoggedIn } from "~/lib/authenticate";
import { getConversation, deleteConversation } from "~/lib/ai";
import { ActionFunction } from "@remix-run/node";
import { redirect } from "@remix-run/node";
export const meta: MetaFunction = () => {
  return [
    { title: "Chat Page" },
    { name: "description", content: "Welcome to Remix!" },
  ];
};

export const loader: LoaderFunction = async ({ request, params }) => {
  await isLoggedIn(request) 
  const res = await getConversation(params?.id || "");
  if (res == null) {
    return json([]);
  }
  return json(res);
};

export const action: ActionFunction = async ({ request, params }) => {
  const user = await isLoggedIn(request)
  if (request.method == "DELETE") {
    const res = await deleteConversation(params?.id || "");
    if (res && res.ok) {
      return redirect("/");
    }
    return null;
  }
};

export default function ConversationRoute() {
  const navigate = useNavigate();

  return (
    <div className="flex h-screen">
      <LeftSide
        onCreateNewChat={() => {
          navigate("/");
        }}
      />
      <RightSide />
    </div>
  );
}
