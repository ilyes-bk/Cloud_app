import {
  updateConversation,
} from "~/lib/ai";
import { ActionFunction, } from "@remix-run/node";
import { isLoggedIn } from "~/lib/authenticate";
export const action: ActionFunction = async ({ request, params }) => {
  const user = await isLoggedIn(request)
  const { id } = params;
  const data = await request.json();

  return updateConversation(id as string, data);
};
