const subjectName = "java";

const COURSE_DATA = {
  subjectName: "Object Oriented Programming Using Java",
  units: [
    {
      unit: "I",
      title: "Basics of Java Programming",
      topics: [
        "Introduction to Java",
        "Basics of Java programming",
        "Data types, Variables, Operators",
        "Control structures including selection, Looping",
        "Java methods, Overloading",
        "Math class",
        "Arrays in java"
      ]
    },
    {
      unit: "II",
      title: "Introduction to Object and Class",
      topics: [
        "Basics of objects and classes in java",
        "Constructors, Finalizer",
        "Visibility modifiers",
        "Methods and objects",
        "Inbuilt classes like String, Character, String Buffer, File",
        "this reference"
      ]
    },
    {
      unit: "III",
      title: "Object Oriented Programming Concepts",
      topics: [
        "Inheritance in java, Super and sub class, Overriding",
        "Object class",
        "Polymorphism, Dynamic binding",
        "Generic programming",
        "Casting objects",
        "Instance of operator",
        "Abstract class",
        "Interface in java",
        "Package in java",
        "UTIL package"
      ]
    },
    {
      unit: "IV",
      title: "Event Handling and GUI Programming",
      topics: [
        "Event handling in java, Event types, Mouse and key events",
        "GUI Basics, Panels, Frames",
        "Layout Managers: Flow Layout, Border Layout, Grid Layout",
        "GUI components like Buttons, Check Boxes, Radio Buttons, Labels, Text Fields, Text Areas, Combo Boxes, Lists, Menus, Dialog Box",
        "Applet and its life cycle"
      ]
    },
    {
      unit: "V",
      title: "Multithreading and Exception Handling",
      topics: [
        "Multithreading in java: Thread life cycle and methods",
        "Runnable interface, Thread synchronization",
        "Exception handling with try-catch-finally",
        "Collections in java",
        "Introduction to JavaBeans and Network Programming"
      ]
    }
  ]
};

if (typeof module !== 'undefined' && module.exports) {
    module.exports = { COURSE_DATA };
}
