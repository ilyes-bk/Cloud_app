import { MetaFunction, useNavigate } from "@remix-run/react";
import { json, LoaderFunction, redirect } from "@remix-run/node";
import LeftSide from "~/components/pages/chat/LeftSide";
import RightSide from "~/components/pages/chat/RightSide";
import { ActionFunction } from "@remix-run/node";
import { deleteTask, getTask, updateTask } from "~/lib/tasks";
import {} from "~/lib/tasks";
import { isLoggedIn } from "~/lib/authenticate";
export const meta: MetaFunction = () => {
  return [
    { title: "Chat Page" },
    { name: "description", content: "Welcome to Remix!" },
  ];
};

export const loader: LoaderFunction = async ({ request, params }) => {
  const res = await getTask(params?.id || "");
  if (res == null) {
    return json([]);
  }
  return json(res);
};

export const action: ActionFunction = async ({ request, params }) => {
  const user = await isLoggedIn(request);
  const { id } = params;
  if (request.method == "DELETE") {
    const res = await deleteTask(params.id || "");
    if (res && res.ok) {
      return redirect("/t");
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
