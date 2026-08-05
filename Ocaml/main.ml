let () =
  let arguments =
    Array.to_list Sys.argv
    |> List.tl
  in

  try
    let result =
      Schreier_sims.est_generateur_from_str arguments
    in

    print_endline (string_of_bool result)

  with
  | Failure message ->
      Printf.eprintf "Error: %s\n" message;
      exit 1

  | Invalid_argument message ->
      Printf.eprintf "Invalid argument: %s\n" message;
      exit 1

  | exception_ ->
      Printf.eprintf "Unexpected OCaml error: %s\n"
        (Printexc.to_string exception_);
      exit 1