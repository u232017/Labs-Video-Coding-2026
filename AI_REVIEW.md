# AI review of Seminar 1

ChatGPT (Codex) reviewed the workspace copy of `seminar1/first_seminar.py` and generated the tests in `seminar1/test_first_seminar.py`. The review covers both classes, all four methods, and all six module-level functions.

## Prompts

These excerpts from the assignment request were used in this session.

- Code review prompt — “Give your repo to an AI (ChatGPT, Claude, Copilot…) and ask for: (a) a **code review**”
- Test prompt — “(b) **unit tests** for each class and method” and “The tests must run (**`pytest`). If a test fails, whose fault is it: yours or the AI's?”
- Scope instruction for both prompts — “make this only for the seminar1 so for the methods and classes of first_seminar.py”

## Review decisions

| Suggestion | Decision | Why |
| --- | --- | --- |
| Run the Exercise 8 demo only when the module is executed as a script. | Accepted | Import previously opened an image, wrote output files, and invoked FFmpeg. The main guard makes the functions importable for tests without those side effects. |
| Convert incoming DCT blocks to floating point before subtracting 128. | Accepted | Subtracting from unsigned 8-bit pixels wrapped values below 128. A regression test now checks the expected negative DC coefficient. |
| Return an empty list when run-length encoding an empty input. | Accepted | An empty sequence has zero runs, and accessing its first element caused an `IndexError`. |
| Mock FFmpeg when testing `image_resize`. | Accepted | This covers argument construction, invalid options, and subprocess errors without requiring FFmpeg or writing any images. |
| Declare `ColorTranslator` methods as static methods. | Rejected | This would enable calling through instances. The exercise uses class calls, which already work. |
| Add explicit input validation for DCT block shape, quantization quality, and empty or ragged zigzag matrices. | Rejected | These calls currently assume valid input. The assignment does not specify an invalid-input contract, so this change leaves those API decisions open. |
| Rename `Runlenght_encode` and `Runlenght_decode` to correct their spelling. | Rejected | Renaming public functions would break callers using the exercise's existing names. |
| Resolve the demo's image paths relative to the script directory. | Rejected | This review keeps the demo's working-directory convention. Unit tests run independently of that convention. |

## Running the tests

From the repository root, with pytest, NumPy, SciPy, and Pillow installed, run:

```sh
pytest -q
```

The final run passed all **46 cases**. This workspace reported warnings about write access to `.pytest_cache`. The same tests can run without the cache using `pytest -q -p no:cacheprovider seminar1`.

## Who owns a failing test?

The first run, after adding the import guard and before fixing the two defects, had **44 passes and 2 failures**. Both failures came from the existing implementation. A constant block of unsigned pixels with value 112 produced a DC coefficient of 120 where the level shift and quantization give −8. Encoding an empty sequence raised `IndexError` where zero runs are expected. Both cases passed after the implementation fixes.

If an AI-generated assertion or fixture contradicts the agreed behavior, the generated test is at fault. If a valid test exposes incorrect behavior, the implementation is at fault. An ambiguous requirement needs clarification before assigning fault. The person submitting the work is responsible for checking the expected behavior, reviewing the fix, and running the suite.
