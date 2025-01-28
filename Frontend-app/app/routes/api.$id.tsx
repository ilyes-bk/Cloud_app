import { ActionFunction } from "@remix-run/node";
import { isLoggedIn } from "~/lib/authenticate";
import { updateTask } from "~/lib/tasks";
export const action: ActionFunction = async ({ request, params }) => {
  const user = await isLoggedIn(request);
  const { id } = params;
  if (request.method == "POST") {
    const data = await request.json();
    const response =  updateTask(id as string, data);
    return response;
  }
};
