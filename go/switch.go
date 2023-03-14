package main

import "fmt"

func main() {
	a := "foo"
	switch a {

	case "foo":
		fmt.Println("in foo")

	case "bar":
		fmt.Println("in bar")
	
	default:
		fmt.Println("default")
	}

	// default block is optional
	
	switch b := 3; b {

	case 1:
		fmt.Println("1")

	case 2:
		fmt.Println("2")

	case 3:
		fmt.Println("3")
	}

	// type switch
	fmt.Println("\n--- type switch ---")
	var foo interface {} = "foo"
	switch t := foo.(type) {

	case int:
		fmt.Println("int | ", t)

	case float32, float64:
		fmt.Println("float | ", t)

	case *int, *bool:  
		fmt.Println("int pointer | string pointer | ", t)

	case string:
		fmt.Println("string | ", t)
	}
}