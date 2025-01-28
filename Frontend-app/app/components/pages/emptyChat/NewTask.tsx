import RightSideHeader from "../chat/Header";
import { useState } from "react";
import { toast, ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

export default function NewChat() {
  const [taskType, setTaskType] = useState<string>("");
  const [action, setAction] = useState<string>("");
  const handleExecute = async () => {
    if(action != ""){
        const response = await fetch('/api?action='+action, {method: 'POST'})
        const data = await response.json()
        toast.info(data?.message || "dafuq")
    } else {
        toast.info("Specify action")
    }
  
  };

  return (
    <div className="flex flex-col w-full min-h-screen ">
      <RightSideHeader />
      <main className="flex-1 overflow-auto items-center justify-center flex">
        <div className="container mx-auto px-4 py-8">
          <div className="max-w-2xl mx-auto text-center">
            <h2 className="text-4xl font-bold mb-4">
              How can I help you today?
            </h2>

            <div className="mb-4">
              <div className="flex space-x-4 mb-2">
                <div className="w-1/2">
                  <label htmlFor="taskType" className="block text-lg font-medium">
                    Task Type
                  </label>
                  <select
                    id="taskType"
                    value={taskType}
                    onChange={(e)=>setTaskType(e.target.value)}
                    className="w-full p-2 border border-gray-300 rounded-md"
                  >
                    <option value="">Select Task Type</option>
                    <option value="followUps">Follow Ups</option>
                  </select>
                </div>

                {/* Action Select */}
                <div className="w-1/2">
                  <label htmlFor="action" className="block text-lg font-medium">
                    Action
                  </label>
                  <select
                    id="action"
                    value={action}
                    onChange={(e)=>setAction(e.target.value)}
                    className="w-full p-2 border border-gray-300 rounded-md"
                    disabled={!taskType} // Disable action until a task type is selected
                  >
                    <option value="">Select Action</option>
                    {taskType === "followUps" && (
                      <>
                        <option value="CREATE_FOLLOW_UPS">Write</option>
                        <option value="DELETE_FOLLOW_UPS">Delete</option>
                      </>
                    )}
                  </select>
                </div>
              </div>
            </div>
            <ToastContainer />
            <div className="mt-4">
              <button
                onClick={handleExecute}
                className="px-6 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600"
              >
                Execute
              </button>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
