import { type MetaFunction } from "@remix-run/node";
import LeftSide from "~/components/pages/chat/LeftSide";
import NewTask from "~/components/pages/emptyChat/NewTask";
import { ActionFunction } from "@remix-run/node";
import { isLoggedIn } from "~/lib/authenticate";
import { getOpenTasks } from "~/lib/tasks";
import { json } from "@remix-run/node";
import { LoaderFunction } from "@remix-run/node";
import { toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';


export const meta: MetaFunction = () => {
  return [
    { title: "Chat Page" },
    { name: "description", content: "Welcome to Remix!" },
  ];
};
export const loader: LoaderFunction = async ({ request }) => {
  const conversations = await getOpenTasks();
  return json(conversations);
};


export default function Index() {

  return (
    <div className="h-screen flex">
      <LeftSide/>
      <NewTask />
    </div>
  );
}
