import { UserNav } from "~/components/UserNav";
import { ModelSelect } from "./ModelSelect";

const RightSideHeader: React.FC = () => {
  return (
    <div className="flex w-full justify-between py-2">
      <ModelSelect />
      <UserNav />
    </div>
  );
};

export default RightSideHeader;
