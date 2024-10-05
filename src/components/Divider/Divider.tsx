interface DividerProps {
  text: string;
  description?: string;
}

const Divider = (props: DividerProps) => {
  return (
    <div className="flex flex-col items-center justify-center bg-black h-24 mx-24 rounded-xl px-72">
      <div className="px-2 mt-2 text-white text-4xl font-extrabold">
        {props.text}
      </div>
      {props.description && (
        <div className="px-2 my-2 text-white text-lg font-medium">
          {props.description}
        </div>
      )}
    </div>
  );
};

export default Divider;