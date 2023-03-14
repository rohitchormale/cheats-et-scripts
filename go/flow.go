package main

import "fmt"

func main() {
	// goto
	fmt.Println("\n--- goto ---")
	fmt.Println("before foo")
	goto foo

	foo:
		fmt.Println("in foo")

	fmt.Println("after foo")

	// if
	fmt.Println("\n--- if ---")
	if true {
		fmt.Println("in if")
	}

	// if-else
	fmt.Println("\n--- if-else ---")
	if false {
		fmt.Println("in if")
	} else {
		fmt.Println("in else")
	}

	// if-else-if-else 
	fmt.Println("\n--- if-else-if-else ---")
	if false {
		fmt.Println("in if")
	} else if true {
		fmt.Println("in else if")
	} else {
		fmt.Println("in else")
	}

	// short
	fmt.Println("\n --- short hand ---")
	if x := func() bool {return true}(); x {
		fmt.Println("in if")
	}
	a := 4
	if b:= 3; a > b {
		fmt.Println("in if")
	}


}

