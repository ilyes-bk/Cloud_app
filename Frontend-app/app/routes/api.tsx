import { ActionFunction } from "@remix-run/node";
import { isLoggedIn } from "~/lib/authenticate";
import { json } from "@remix-run/node";
const ENDPOINT = "http://backend:8000";
export const action: ActionFunction = async ({ request, params }) => {
  const user = await isLoggedIn(request);
  const url = new URL(request.url);
  const action = url.searchParams.get("action") || "";
  if(action){
    return fetch(ENDPOINT + "/tasks?action=" + action, {method: 'POST'})
  }
  return json({message: 'specify action'})
};
