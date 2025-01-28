import { getConversations, newConversation} from "~/lib/ai";
import { ActionFunction, LoaderFunction } from "@remix-run/node";
import { json } from "@remix-run/node";
import { isLoggedIn } from "~/lib/authenticate";
export const loader: LoaderFunction = async ({ request }) => {
    const conversations = await getConversations();
    return json( conversations );
  };

  export const action:  ActionFunction= async ({ request }) => {
    const user = await isLoggedIn(request)
    const data = await request.json();
    return newConversation(data)
  };